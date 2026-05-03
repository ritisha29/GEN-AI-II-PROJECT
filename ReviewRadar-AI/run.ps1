$ErrorActionPreference = "Stop"

Write-Host "=== ReviewRadar AI Runner ===" -ForegroundColor Cyan
Write-Host "Setting up environment..."

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Ensure execution policy allows script execution (for current process)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Activate venv
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Ensuring dependencies are installed..."
pip install -r requirements.txt

# Start the server
Write-Host "Starting FastAPI server..." -ForegroundColor Green
Write-Host "The application will be available at http://localhost:8000" -ForegroundColor Yellow
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
