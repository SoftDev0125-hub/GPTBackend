"""
App Control Service - Handles starting and stopping applications
"""
import os
import subprocess
import asyncio
import psutil
from typing import Dict, List
import json

# Default app configurations
DEFAULT_APPS = {
    "notepad": {
        "path": "notepad.exe",
        "type": "executable"
    },
    "calculator": {
        "path": "calc.exe",
        "type": "executable"
    },
    "chrome": {
        "path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "type": "executable"
    },
    "firefox": {
        "path": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "type": "executable"
    },
    "vscode": {
        "path": "code",
        "type": "command"
    }
}


class AppControlService:
    def __init__(self):
        self.config_path = os.getenv('APP_CONFIG_PATH', 'app_config.json')
        self.app_configs = self._load_config()

    def _load_config(self) -> Dict:
        """Load app configurations from file or use defaults"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults
                    merged = DEFAULT_APPS.copy()
                    merged.update(config)
                    return merged
            except Exception as e:
                print(f"Error loading app config: {e}")
                return DEFAULT_APPS
        return DEFAULT_APPS

    def _save_config(self):
        """Save app configurations to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.app_configs, f, indent=2)
        except Exception as e:
            print(f"Error saving app config: {e}")

    async def start_app(self, app_name: str) -> Dict[str, any]:
        """Start an application"""
        app_name_lower = app_name.lower()
        
        # Check if app is already running
        if await self._is_app_running(app_name_lower):
            return {
                "success": True,
                "message": f"{app_name} is already running"
            }
        
        # Get app configuration
        app_config = self.app_configs.get(app_name_lower)
        if not app_config:
            return {
                "success": False,
                "message": f"App '{app_name}' not found in configuration. Use /apps/list to see available apps."
            }
        
        try:
            if app_config["type"] == "executable":
                # Start executable
                process = await asyncio.create_subprocess_exec(
                    app_config["path"],
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            elif app_config["type"] == "command":
                # Start command (like 'code' for VS Code)
                process = await asyncio.create_subprocess_shell(
                    app_config["path"],
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            else:
                return {
                    "success": False,
                    "message": f"Unknown app type: {app_config['type']}"
                }
            
            # Don't wait for process to finish
            return {
                "success": True,
                "message": f"{app_name} started successfully",
                "pid": process.pid
            }
        except FileNotFoundError:
            return {
                "success": False,
                "message": f"Application not found at path: {app_config['path']}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error starting {app_name}: {str(e)}"
            }

    async def stop_app(self, app_name: str) -> Dict[str, any]:
        """Stop an application"""
        app_name_lower = app_name.lower()
        
        # Check if app is running
        if not await self._is_app_running(app_name_lower):
            return {
                "success": True,
                "message": f"{app_name} is not running"
            }
        
        # Get app configuration
        app_config = self.app_configs.get(app_name_lower)
        if not app_config:
            return {
                "success": False,
                "message": f"App '{app_name}' not found in configuration"
            }
        
        try:
            # Find and kill processes
            killed_count = 0
            process_name = os.path.basename(app_config["path"]).lower()
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] and process_name in proc.info['name'].lower():
                        proc.kill()
                        killed_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            if killed_count > 0:
                return {
                    "success": True,
                    "message": f"Stopped {killed_count} instance(s) of {app_name}"
                }
            else:
                return {
                    "success": False,
                    "message": f"Could not find running instances of {app_name}"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error stopping {app_name}: {str(e)}"
            }

    async def _is_app_running(self, app_name: str) -> bool:
        """Check if an app is currently running"""
        app_config = self.app_configs.get(app_name)
        if not app_config:
            return False
        
        try:
            process_name = os.path.basename(app_config["path"]).lower()
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] and process_name in proc.info['name'].lower():
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            return False
        except Exception:
            return False

    async def list_available_apps(self) -> List[Dict[str, str]]:
        """List all available apps that can be controlled"""
        apps = []
        for name, config in self.app_configs.items():
            is_running = await self._is_app_running(name)
            apps.append({
                "name": name,
                "path": config.get("path", ""),
                "type": config.get("type", "unknown"),
                "running": is_running
            })
        return apps

    def add_app(self, name: str, path: str, app_type: str = "executable"):
        """Add a new app to the configuration"""
        self.app_configs[name.lower()] = {
            "path": path,
            "type": app_type
        }
        self._save_config()

    def remove_app(self, name: str):
        """Remove an app from the configuration"""
        if name.lower() in self.app_configs:
            del self.app_configs[name.lower()]
            self._save_config()

