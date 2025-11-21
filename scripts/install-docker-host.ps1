# Installation script for Docker with Host Access (Windows PowerShell)
# This script sets up Package Audit Dashboard with full host system access

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Package Audit Dashboard - Docker Host Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
$dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerInstalled) {
    Write-Host "❌ Error: Docker is not installed" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
}

Write-Host "✅ Docker installed: $(docker --version)" -ForegroundColor Green

# Check if Docker Compose is available (plugin version preferred)
$composeVersion = docker compose version 2>&1
$composeStandalone = Get-Command docker-compose -ErrorAction SilentlyContinue

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker Compose (plugin): $composeVersion" -ForegroundColor Green
} elseif ($composeStandalone) {
    Write-Host "✅ Docker Compose (standalone): $(docker-compose --version)" -ForegroundColor Green
    Write-Host "ℹ️  Note: Consider upgrading to Docker Desktop with integrated Compose plugin" -ForegroundColor Cyan
} else {
    Write-Host "❌ Error: Docker Compose is not available" -ForegroundColor Red
    Write-Host "Please ensure Docker Desktop is properly installed"
    exit 1
}
Write-Host ""

# Check if Docker daemon is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Docker daemon is not running" -ForegroundColor Red
    Write-Host "Please start Docker Desktop"
    exit 1
}
Write-Host ""

# Detect Windows version
$OSVersion = [System.Environment]::OSVersion.Version
Write-Host "🪟 Detected: Windows $($OSVersion.Major).$($OSVersion.Minor)" -ForegroundColor Yellow

# Check for WSL2
$wslInstalled = Get-Command wsl -ErrorAction SilentlyContinue
if ($wslInstalled) {
    Write-Host "🔷 WSL2 detected - Docker can use WSL2 backend" -ForegroundColor Cyan
}
Write-Host ""

# Create data directory
$DataDir = Join-Path $ProjectRoot "data"
if (-not (Test-Path $DataDir)) {
    New-Item -ItemType Directory -Path $DataDir | Out-Null
}
Write-Host "✅ Created data directory: $DataDir" -ForegroundColor Green

# Copy environment configuration
$EnvFile = Join-Path $ProjectRoot ".env"
$EnvHostFile = Join-Path $ProjectRoot ".env.host"

if (Test-Path $EnvFile) {
    Write-Host "⚠️  .env file already exists" -ForegroundColor Yellow
    $overwrite = Read-Host "Overwrite with host access configuration? (y/N)"
    if ($overwrite -eq "y" -or $overwrite -eq "Y") {
        Copy-Item $EnvHostFile $EnvFile -Force
        Write-Host "✅ Updated .env with host access configuration" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  Keeping existing .env file" -ForegroundColor Cyan
    }
} else {
    Copy-Item $EnvHostFile $EnvFile
    Write-Host "✅ Created .env with host access configuration" -ForegroundColor Green
}
Write-Host ""

# Update .env with Windows-specific settings
Write-Host "Configuring Windows-specific settings..." -ForegroundColor Cyan

# Convert Windows paths to Docker-compatible format
$UserProfile = $env:USERPROFILE -replace '\\', '/'
$ProgramFiles = ${env:ProgramFiles} -replace '\\', '/'
$SystemRoot = $env:SystemRoot -replace '\\', '/'

# Update .env file
$envContent = Get-Content $EnvFile
$envContent = $envContent -replace 'HOST_DATA_DIR=\./data', "HOST_DATA_DIR=$($DataDir -replace '\\', '/')"
$envContent = $envContent -replace 'WINDOWS_USER_PROFILE=.*', "WINDOWS_USER_PROFILE=$UserProfile"
$envContent = $envContent -replace 'WINDOWS_PROGRAMFILES=.*', "WINDOWS_PROGRAMFILES=$ProgramFiles"
$envContent = $envContent -replace 'WINDOWS_SYSTEM32=.*', "WINDOWS_SYSTEM32=$SystemRoot/System32"
$envContent | Set-Content $EnvFile

Write-Host "✅ Configured Windows paths" -ForegroundColor Green
Write-Host ""

# Security warning
Write-Host "⚠️  Security Warning: Privileged Mode" -ForegroundColor Yellow
Write-Host "Privileged mode gives the container full access to the host system."
Write-Host "This is required for some operations but has security implications."
Write-Host ""
$privileged = Read-Host "Enable privileged mode? (y/N)"
if ($privileged -eq "y" -or $privileged -eq "Y") {
    $envContent = Get-Content $EnvFile
    $envContent = $envContent -replace 'DOCKER_PRIVILEGED=false', 'DOCKER_PRIVILEGED=true'
    $envContent | Set-Content $EnvFile
    Write-Host "✅ Privileged mode enabled" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Privileged mode disabled (default)" -ForegroundColor Cyan
}
Write-Host ""

# Build Docker images
Write-Host "Building Docker images..." -ForegroundColor Cyan
Set-Location $ProjectRoot
docker compose -f docker-compose.host.yml build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to build Docker images" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker images built successfully" -ForegroundColor Green
Write-Host ""

# Start services
Write-Host "Starting services..." -ForegroundColor Cyan
docker compose -f docker-compose.host.yml up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start services" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Services started" -ForegroundColor Green
Write-Host ""

# Wait for services to be ready
Write-Host "Waiting for services to be ready..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# Check service health
$psOutput = docker compose -f docker-compose.host.yml ps
if ($psOutput -match "Up") {
    Write-Host "✅ Services are running" -ForegroundColor Green
} else {
    Write-Host "⚠️  Warning: Some services may not be running" -ForegroundColor Yellow
    Write-Host "Check status with: docker compose -f docker-compose.host.yml ps"
}
Write-Host ""

# Display access information
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🎉 Installation Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Services are now running with HOST ACCESS enabled:" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Frontend Dashboard: http://localhost:5173" -ForegroundColor White
Write-Host "🔌 Backend API:        http://localhost:8000" -ForegroundColor White
Write-Host "📚 API Documentation:  http://localhost:8000/docs" -ForegroundColor White
Write-Host "❤️  Health Check:       http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "Host Access Configuration:" -ForegroundColor Cyan
Write-Host "  • Data directory:  $DataDir"
Write-Host "  • User profile:    $UserProfile"
Write-Host "  • Program Files:   $ProgramFiles"
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  • View logs:       docker compose -f docker-compose.host.yml logs -f"
Write-Host "  • Stop services:   docker compose -f docker-compose.host.yml stop"
Write-Host "  • Restart:         docker compose -f docker-compose.host.yml restart"
Write-Host "  • Remove all:      docker compose -f docker-compose.host.yml down -v"
Write-Host ""
Write-Host "⚠️  Important Notes:" -ForegroundColor Yellow
Write-Host "  1. The container can now access your host system"
Write-Host "  2. This includes executing commands and accessing files"
Write-Host "  3. Review security implications in docs/SECURITY.md"
Write-Host "  4. Adjust .env configuration as needed"
Write-Host ""
Write-Host "Windows-Specific Notes:" -ForegroundColor Yellow
Write-Host "  1. Ensure Docker Desktop is set to use WSL2 backend (recommended)"
Write-Host "  2. Share necessary drives in Docker Desktop settings"
Write-Host "  3. You may need to allow Docker through Windows Firewall"
Write-Host ""
Write-Host "📖 For more information, see:" -ForegroundColor Cyan
Write-Host "  • docs/INSTALLATION.md"
Write-Host "  • docs/USAGE.md"
Write-Host "  • docs/DOCKER.md"
Write-Host ""
