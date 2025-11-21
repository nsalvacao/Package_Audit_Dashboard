#!/bin/bash
# Test script for Docker Host Access installation
# This script validates the Docker host access configuration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================="
echo "Docker Host Access - Configuration Test"
echo "=========================================="
echo ""

cd "$PROJECT_ROOT"

# Test 1: Check Docker availability
echo "Test 1: Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ FAIL: Docker not installed"
    exit 1
fi
echo "✅ PASS: Docker installed ($(docker --version))"
echo ""

# Test 2: Check Docker Compose availability
echo "Test 2: Checking Docker Compose..."
if ! docker compose version &> /dev/null; then
    echo "❌ FAIL: Docker Compose not available"
    exit 1
fi
echo "✅ PASS: Docker Compose available ($(docker compose version))"
echo ""

# Test 3: Validate docker-compose.host.yml
echo "Test 3: Validating docker-compose.host.yml..."
if ! docker compose -f docker-compose.host.yml config --quiet 2>&1; then
    echo "❌ FAIL: docker-compose.host.yml is invalid"
    exit 1
fi
echo "✅ PASS: docker-compose.host.yml is valid"
echo ""

# Test 4: Check if .env.host exists
echo "Test 4: Checking .env.host template..."
if [ ! -f ".env.host" ]; then
    echo "❌ FAIL: .env.host not found"
    exit 1
fi
echo "✅ PASS: .env.host template exists"
echo ""

# Test 5: Check Dockerfile.host exists
echo "Test 5: Checking Dockerfile.host..."
if [ ! -f "backend/Dockerfile.host" ]; then
    echo "❌ FAIL: backend/Dockerfile.host not found"
    exit 1
fi
echo "✅ PASS: Dockerfile.host exists"
echo ""

# Test 6: Check installation scripts
echo "Test 6: Checking installation scripts..."
if [ ! -f "scripts/install-docker-host.sh" ] || [ ! -f "scripts/install-docker-host.ps1" ]; then
    echo "❌ FAIL: Installation scripts not found"
    exit 1
fi
echo "✅ PASS: Installation scripts exist"
echo ""

# Test 7: Verify host_executor.py syntax
echo "Test 7: Validating host_executor.py syntax..."
if ! python3 -m py_compile backend/app/core/host_executor.py 2>&1; then
    echo "❌ FAIL: host_executor.py has syntax errors"
    exit 1
fi
echo "✅ PASS: host_executor.py syntax is valid"
echo ""

# Test 8: Check documentation
echo "Test 8: Checking documentation..."
if [ ! -f "docs/INSTALLATION.md" ] || [ ! -f "docs/USAGE.md" ]; then
    echo "❌ FAIL: Documentation files missing"
    exit 1
fi
echo "✅ PASS: Documentation exists"
echo ""

# Summary
echo "=========================================="
echo "✅ All Tests Passed!"
echo "=========================================="
echo ""
echo "Configuration is ready for Docker host access."
echo ""
echo "To install and run:"
echo "  Linux/macOS/WSL: ./scripts/install-docker-host.sh"
echo "  Windows:         .\scripts\install-docker-host.ps1"
echo ""
echo "For more information:"
echo "  Installation: docs/INSTALLATION.md"
echo "  Usage:        docs/USAGE.md"
echo "  Docker:       docs/DOCKER.md"
echo ""
