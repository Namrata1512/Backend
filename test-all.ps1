# test-all.ps1
Write-Host "`n=== BACKEND ASSESSMENT - COMPLETE TEST SUITE ===" -ForegroundColor Cyan
Write-Host "Author: Namrata R Gachchi`n" -ForegroundColor Gray

# Flask Tests
Write-Host "`n[1/7] Testing Flask Health..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/health"
    Write-Host "Success - Flask is healthy" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json
} catch {
    Write-Host "Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n[2/7] Testing Flask Pagination..." -ForegroundColor Yellow
try {
    $url = "http://localhost:5000/api/customers?page=1&limit=5"
    $response = Invoke-WebRequest -Uri $url
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Success - Retrieved $($data.data.Count) of $($data.total) customers" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n[3/7] Testing Flask Single Customer..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/customers/CUST001"
    Write-Host "Success - Retrieved customer CUST001" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# FastAPI Tests
Write-Host "`n[4/7] Testing FastAPI Health..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health"
    Write-Host "Success - FastAPI is healthy" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json
} catch {
    Write-Host "Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n[5/7] Testing Data Ingestion (Flask -> PostgreSQL)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/ingest" -Method POST
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Success - Ingested $($data.records_processed) records successfully" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json
} catch {
    Write-Host "Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n[6/7] Testing FastAPI Database Query (Pagination)..." -ForegroundColor Yellow
try {
    $url = "http://localhost:8000/api/customers?page=1&limit=5"
    $response = Invoke-WebRequest -Uri $url
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Success - Retrieved $($data.data.Count) of $($data.total) customers from database" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n[7/7] Testing FastAPI Single Customer from Database..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/customers/CUST001"
    Write-Host "Success - Retrieved customer CUST001 from database" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== ALL TESTS COMPLETE ===" -ForegroundColor Cyan
Write-Host "If all tests passed, your project is ready for submission!`n" -ForegroundColor Green