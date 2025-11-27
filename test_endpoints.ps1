# PowerShell script to test all endpoints
param(
    [string]$BaseUrl = "http://localhost:8000"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GPT Backend API - Endpoint Tests" -ForegroundColor Cyan
Write-Host "======================================`n" -ForegroundColor Cyan

# Test 1: Health Check
Write-Host "[TEST 1] Health Check" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/health" -UseBasicParsing
    Write-Host "  Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  Response: $($response.Content)`n"
} catch {
    Write-Host "  ERROR: $_`n" -ForegroundColor Red
}

# Test 2: Root endpoint
Write-Host "[TEST 2] Root Endpoint" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/" -UseBasicParsing
    Write-Host "  Status: $($response.StatusCode)" -ForegroundColor Green
    $json = $response.Content | ConvertFrom-Json
    Write-Host "  Service: $($json.service)"
    Write-Host "  Version: $($json.version)`n"
} catch {
    Write-Host "  ERROR: $_`n" -ForegroundColor Red
}

# Test 3: Gmail Auth Status
Write-Host "[TEST 3] Gmail Authentication Status" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/gmail/auth/status" -UseBasicParsing
    $json = $response.Content | ConvertFrom-Json
    if ($json.authenticated) {
        Write-Host "  Status: Authenticated" -ForegroundColor Green
    } else {
        Write-Host "  Status: Not authenticated" -ForegroundColor Yellow
    }
    Write-Host "  Message: $($json.message)`n"
} catch {
    Write-Host "  ERROR: $_`n" -ForegroundColor Red
}

# Test 4: List Apps
Write-Host "[TEST 4] List Available Apps" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/apps/list" -UseBasicParsing
    $json = $response.Content | ConvertFrom-Json
    Write-Host "  Found $($json.apps.Count) apps:" -ForegroundColor Green
    foreach ($app in $json.apps) {
        $status = if ($app.running) { "Running" } else { "Stopped" }
        Write-Host "    - $($app.name): $status"
    }
    Write-Host ""
} catch {
    Write-Host "  ERROR: $_`n" -ForegroundColor Red
}

# Test 5: Read Gmail Messages (if authenticated)
Write-Host "[TEST 5] Read Gmail Messages" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/gmail/messages?max_results=3" -UseBasicParsing
    $messages = $response.Content | ConvertFrom-Json
    Write-Host "  Found $($messages.Count) messages" -ForegroundColor Green
    if ($messages.Count -gt 0) {
        Write-Host "  First message:" -ForegroundColor Cyan
        Write-Host "    From: $($messages[0].from_email)"
        Write-Host "    Subject: $($messages[0].subject)"
    }
    Write-Host ""
} catch {
    Write-Host "  ERROR: $_ (Gmail may not be authenticated)`n" -ForegroundColor Yellow
}

# Test 6: Start an App
Write-Host "[TEST 6] Start Notepad" -ForegroundColor Yellow
try {
    $body = @{
        app_name = "notepad"
        action = "start"
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "$BaseUrl/apps/control" -Method POST -Body $body -ContentType "application/json"
    $result = $response.Content | ConvertFrom-Json
    if ($result.success) {
        Write-Host "  Success: $($result.message)" -ForegroundColor Green
    } else {
        Write-Host "  Failed: $($result.message)" -ForegroundColor Yellow
    }
    Write-Host ""
} catch {
    Write-Host "  ERROR: $_`n" -ForegroundColor Red
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Tests Completed!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nFor interactive testing, visit: $BaseUrl/docs" -ForegroundColor Green

