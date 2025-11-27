"""
Simple script to run the server
"""
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"Starting server on http://{host}:{port}")
    print(f"API docs available at http://{host}:{port}/docs")
    print(f"OpenAPI schema at http://{host}:{port}/openapi.json")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )

