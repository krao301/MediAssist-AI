# MediAssist AI - Quick Start Script (PowerShell)
# Usage: .\start.ps1 [backend|frontend|docker|all]

param(
    [string]$Mode = "all"
)

function Start-Backend {
    Write-Host "🚀 Starting Backend API..." -ForegroundColor Green
    Set-Location api
    
    if (-not (Test-Path ".venv")) {
        Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
        python -m venv .venv
    }
    
    .\.venv\Scripts\Activate.ps1
    pip install -q -r requirements.txt
    
    if (-not (Test-Path ".env")) {
        Write-Host "⚠️  No .env file found. Creating from example..." -ForegroundColor Yellow
        Copy-Item .env.example .env
        Write-Host "📝 Please edit api\.env with your API keys before continuing." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Backend ready on http://localhost:8000" -ForegroundColor Green
    uvicorn app.main:app --reload --port 8000
}

function Start-Frontend {
    Write-Host "🚀 Starting Frontend PWA..." -ForegroundColor Green
    Set-Location web
    
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing npm dependencies..." -ForegroundColor Yellow
        npm install
    }
    
    if (-not (Test-Path ".env")) {
        Write-Host "⚠️  No .env file found. Creating from example..." -ForegroundColor Yellow
        Copy-Item .env.example .env
    }
    
    Write-Host "✅ Frontend ready on http://localhost:5173" -ForegroundColor Green
    npm run dev
}

function Start-Docker {
    Write-Host "🐳 Starting Docker services..." -ForegroundColor Green
    Set-Location infra
    docker-compose up -d
    Write-Host "✅ Services started:" -ForegroundColor Green
    Write-Host "   - PostgreSQL: localhost:5432"
    Write-Host "   - Redis: localhost:6379"
    Write-Host "   - API: http://localhost:8000"
}

switch ($Mode) {
    "backend" {
        Start-Backend
    }
    "frontend" {
        Start-Frontend
    }
    "docker" {
        Start-Docker
    }
    "all" {
        Write-Host "🎯 Starting all services..." -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Option 1: Docker (Recommended)" -ForegroundColor Yellow
        Write-Host "  .\start.ps1 docker"
        Write-Host ""
        Write-Host "Option 2: Manual" -ForegroundColor Yellow
        Write-Host "  Terminal 1: .\start.ps1 backend"
        Write-Host "  Terminal 2: .\start.ps1 frontend"
        Write-Host ""
        Write-Host "Choose your method and run the appropriate command."
    }
    default {
        Write-Host "Usage: .\start.ps1 [backend|frontend|docker|all]" -ForegroundColor Red
        exit 1
    }
}
