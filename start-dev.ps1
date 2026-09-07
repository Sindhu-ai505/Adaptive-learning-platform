# start-dev.ps1 — starts backend and frontend dev servers in separate windows
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Starting AdaptiveLearn dev servers..." -ForegroundColor Cyan

# Backend
Start-Process powershell -ArgumentList @(
  "-NoExit", "-Command",
  "cd '$root\backend'; " +
  '$env:DATABASE_URL="sqlite:///./adaptive_learning.db"; ' +
  '$env:SECRET_KEY="dev-secret-key-change-before-any-production-use"; ' +
  '$env:ALLOWED_ORIGINS="http://localhost:5173"; ' +
  '..\\.venv\\Scripts\\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000 --reload'
) -WindowStyle Normal

Start-Sleep -Seconds 2

# Frontend
Start-Process powershell -ArgumentList @(
  "-NoExit", "-Command",
  "cd '$root\frontend'; npx vite --port 5173"
) -WindowStyle Normal

Write-Host ""
Write-Host "  Backend  → http://localhost:8000" -ForegroundColor Green
Write-Host "  API docs → http://localhost:8000/docs" -ForegroundColor Green
Write-Host "  Frontend → http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "Both servers starting in separate windows." -ForegroundColor Yellow
