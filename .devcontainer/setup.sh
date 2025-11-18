#!/bin/bash

# Codespaces Post-Create Setup Script
# This script runs automatically after the Codespace is created

set -e

echo "🚀 Starting Package Audit Dashboard setup for GitHub Codespaces..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Navigate to workspace
cd /workspace

# =====================================
# Backend Setup
# =====================================
print_step "Setting up Python backend..."

cd backend

# Create and activate virtual environment
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    print_success "Created Python virtual environment"
fi

source .venv/bin/activate

# Install Python dependencies
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt
print_success "Installed Python dependencies"

# Install development tools
pip install black flake8 mypy pytest-cov ipython > /dev/null 2>&1
print_success "Installed Python development tools"

# Install CLI tool
if [ -d "../cli" ]; then
    pip install -e ../cli
    print_success "Installed CLI tool"
fi

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_success "Created backend .env file"
fi

# Create data directory
mkdir -p data/{snapshots,logs}
print_success "Created data directories"

cd ..

# =====================================
# Frontend Setup
# =====================================
print_step "Setting up React frontend..."

cd frontend

# Install Node dependencies
npm install --silent
print_success "Installed Node dependencies"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    # Update API URL for Codespaces
    echo "VITE_API_URL=http://localhost:8000" > .env
    print_success "Created frontend .env file"
fi

cd ..

# =====================================
# Git Configuration
# =====================================
print_step "Configuring Git..."

# Set up git hooks (if pre-commit is configured)
if [ -f ".pre-commit-config.yaml" ]; then
    cd backend
    source .venv/bin/activate
    pip install pre-commit > /dev/null 2>&1
    pre-commit install
    print_success "Configured pre-commit hooks"
    cd ..
fi

# =====================================
# GitHub CLI Configuration
# =====================================
if command -v gh &> /dev/null; then
    print_step "GitHub CLI detected"
    print_warning "Run 'gh auth login' to authenticate with GitHub"
fi

# =====================================
# Quick Test
# =====================================
print_step "Running quick health check..."

cd backend
source .venv/bin/activate

# Run a simple test to verify setup
if python -c "import fastapi; import pytest; import typer" 2>/dev/null; then
    print_success "Backend dependencies verified"
else
    print_warning "Some backend dependencies may be missing"
fi

cd ../frontend

if [ -d "node_modules" ]; then
    print_success "Frontend dependencies verified"
else
    print_warning "Frontend dependencies may be incomplete"
fi

cd ..

# =====================================
# Create helpful scripts
# =====================================
print_step "Creating convenience scripts..."

# Start all services script
cat > start-all.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Package Audit Dashboard..."

# Start backend in background
echo "Starting backend on http://localhost:8000..."
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend
echo "Starting frontend on http://localhost:5173..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✓ Backend running on http://localhost:8000 (PID: $BACKEND_PID)"
echo "✓ Frontend running on http://localhost:5173 (PID: $FRONTEND_PID)"
echo ""
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop, press Ctrl+C or run: kill $BACKEND_PID $FRONTEND_PID"

wait
EOF

chmod +x start-all.sh
print_success "Created start-all.sh script"

# Test backend script
cat > test-backend.sh << 'EOF'
#!/bin/bash
cd backend
source .venv/bin/activate
pytest tests/ -v --cov=app --cov-report=html
echo ""
echo "📊 Coverage report: backend/htmlcov/index.html"
EOF

chmod +x test-backend.sh
print_success "Created test-backend.sh script"

# =====================================
# Final Instructions
# =====================================
echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📚 Quick Start Guide:"
echo ""
echo "  1️⃣  Start all services:"
echo "      ./start-all.sh"
echo ""
echo "  2️⃣  Or start individually:"
echo "      Backend:  cd backend && source .venv/bin/activate && uvicorn app.main:app --reload"
echo "      Frontend: cd frontend && npm run dev"
echo ""
echo "  3️⃣  Run tests:"
echo "      ./test-backend.sh"
echo ""
echo "  4️⃣  Use the CLI:"
echo "      cd backend && source .venv/bin/activate"
echo "      python -m cli.audit_cli --help"
echo ""
echo "🤖 GitHub Copilot:"
echo "   - Press Ctrl+I for inline chat"
echo "   - Use @workspace to ask about the codebase"
echo "   - Open Copilot Chat in sidebar for detailed discussions"
echo ""
echo "🔗 Useful URLs (will auto-forward in Codespaces):"
echo "   • Frontend:    http://localhost:5173"
echo "   • Backend:     http://localhost:8000"
echo "   • API Docs:    http://localhost:8000/docs"
echo ""
echo "📖 Documentation:"
echo "   • README.md - Project overview"
echo "   • docs/CODESPACES.md - Codespaces guide"
echo "   • docs/API.md - API documentation"
echo ""
echo "════════════════════════════════════════════════════════════════"
