#!/bin/bash
# Installation script for Docker with Host Access
# This script sets up Package Audit Dashboard with full host system access

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================="
echo "Package Audit Dashboard - Docker Host Setup"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker Compose is installed
COMPOSE_VERSION=""
if docker compose version &> /dev/null; then
    COMPOSE_VERSION="plugin ($(docker compose version))"
    echo "✅ Docker Compose (plugin): $COMPOSE_VERSION"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION="standalone ($(docker-compose --version))"
    echo "✅ Docker Compose (standalone): $COMPOSE_VERSION"
else
    echo "❌ Error: Docker Compose is not installed"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker installed: $(docker --version)"
echo ""

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker daemon is not running"
    echo "Please start Docker Desktop"
    exit 1
fi

echo "✅ Docker daemon is running"
echo ""

# Detect operating system
OS_TYPE="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
    echo "🐧 Detected: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macos"
    echo "🍎 Detected: macOS"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS_TYPE="windows"
    echo "🪟 Detected: Windows (Git Bash/Cygwin)"
elif grep -qi microsoft /proc/version 2>/dev/null; then
    OS_TYPE="wsl"
    echo "🔷 Detected: WSL2"
else
    echo "⚠️  Warning: Unknown OS type: $OSTYPE"
fi
echo ""

# Create data directory
DATA_DIR="$PROJECT_ROOT/data"
mkdir -p "$DATA_DIR"
echo "✅ Created data directory: $DATA_DIR"

# Copy environment configuration
ENV_FILE="$PROJECT_ROOT/.env"
ENV_HOST_FILE="$PROJECT_ROOT/.env.host"

if [ -f "$ENV_FILE" ]; then
    echo "⚠️  .env file already exists"
    read -p "Overwrite with host access configuration? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp "$ENV_HOST_FILE" "$ENV_FILE"
        echo "✅ Updated .env with host access configuration"
    else
        echo "ℹ️  Keeping existing .env file"
    fi
else
    cp "$ENV_HOST_FILE" "$ENV_FILE"
    echo "✅ Created .env with host access configuration"
fi
echo ""

# Update .env with OS-specific settings
echo "Configuring OS-specific settings..."
case $OS_TYPE in
    linux)
        sed -i 's/DOCKER_NETWORK_MODE=bridge/DOCKER_NETWORK_MODE=host/' "$ENV_FILE" 2>/dev/null || true
        echo "✅ Configured for Linux (host networking)"
        ;;
    wsl)
        sed -i 's/DOCKER_NETWORK_MODE=bridge/DOCKER_NETWORK_MODE=bridge/' "$ENV_FILE" 2>/dev/null || true
        echo "✅ Configured for WSL2"
        ;;
    macos|windows)
        sed -i 's/DOCKER_NETWORK_MODE=bridge/DOCKER_NETWORK_MODE=bridge/' "$ENV_FILE" 2>/dev/null || sed '' 2>/dev/null || true
        echo "✅ Configured for $OS_TYPE"
        ;;
esac
echo ""

# Check for WSL2-specific configuration
if [ "$OS_TYPE" == "wsl" ]; then
    echo "WSL2 detected - Additional configuration:"
    echo "1. Ensure Docker Desktop is running on Windows"
    echo "2. Enable WSL2 integration in Docker Desktop settings"
    echo "3. Windows drives are accessible at /mnt/c, /mnt/d, etc."
    echo ""
fi

# Ask user about privileged mode
echo "⚠️  Security Warning: Privileged Mode"
echo "Privileged mode gives the container full access to the host system."
echo "This is required for some operations but has security implications."
echo ""
read -p "Enable privileged mode? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sed -i 's/DOCKER_PRIVILEGED=false/DOCKER_PRIVILEGED=true/' "$ENV_FILE" 2>/dev/null || \
        sed -i '' 's/DOCKER_PRIVILEGED=false/DOCKER_PRIVILEGED=true/' "$ENV_FILE" 2>/dev/null || true
    echo "✅ Privileged mode enabled"
else
    echo "ℹ️  Privileged mode disabled (default)"
fi
echo ""

# Build Docker images
echo "Building Docker images..."
cd "$PROJECT_ROOT"
docker-compose -f docker-compose.host.yml build
echo "✅ Docker images built successfully"
echo ""

# Start services
echo "Starting services..."
docker-compose -f docker-compose.host.yml up -d
echo "✅ Services started"
echo ""

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check service health
if docker-compose -f docker-compose.host.yml ps | grep -q "Up"; then
    echo "✅ Services are running"
else
    echo "⚠️  Warning: Some services may not be running"
    echo "Check status with: docker-compose -f docker-compose.host.yml ps"
fi
echo ""

# Display access information
echo "=========================================="
echo "🎉 Installation Complete!"
echo "=========================================="
echo ""
echo "Services are now running with HOST ACCESS enabled:"
echo ""
echo "📊 Frontend Dashboard: http://localhost:5173"
echo "🔌 Backend API:        http://localhost:8000"
echo "📚 API Documentation:  http://localhost:8000/docs"
echo "❤️  Health Check:       http://localhost:8000/health"
echo ""
echo "Host Access Configuration:"
echo "  • Data directory:  $DATA_DIR"
echo "  • Execution mode:  $(grep HOST_EXECUTION_MODE "$ENV_FILE" | cut -d'=' -f2)"
echo "  • Network mode:    $(grep DOCKER_NETWORK_MODE "$ENV_FILE" | cut -d'=' -f2)"
echo ""
echo "Useful commands:"
echo "  • View logs:       docker-compose -f docker-compose.host.yml logs -f"
echo "  • Stop services:   docker-compose -f docker-compose.host.yml stop"
echo "  • Restart:         docker-compose -f docker-compose.host.yml restart"
echo "  • Remove all:      docker-compose -f docker-compose.host.yml down -v"
echo ""
echo "⚠️  Important Notes:"
echo "  1. The container can now access your host system"
echo "  2. This includes executing commands and accessing files"
echo "  3. Review security implications in docs/SECURITY.md"
echo "  4. Adjust .env configuration as needed"
echo ""
echo "📖 For more information, see:"
echo "  • docs/INSTALLATION.md"
echo "  • docs/USAGE.md"
echo "  • docs/DOCKER.md"
echo ""
