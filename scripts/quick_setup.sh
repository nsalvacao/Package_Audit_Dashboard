#!/bin/bash
set -e

echo "🚀 Package Audit Dashboard - Quick Setup"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📌 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1,2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
echo ""

# Setup Backend
echo "🔧 Setting up Backend..."
cd backend

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v --tb=short
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${YELLOW}⚠ Some tests failed (this is expected if system package managers are not installed)${NC}"
fi
echo ""

cd ..

# Check Node.js for frontend
echo "📌 Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"

    if [ -d "frontend" ]; then
        echo "🔧 Setting up Frontend..."
        cd frontend

        if [ ! -d "node_modules" ]; then
            echo "Installing npm dependencies..."
            npm install
            echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
        else
            echo -e "${YELLOW}⚠ Frontend dependencies already installed${NC}"
        fi

        cd ..
    else
        echo -e "${YELLOW}⚠ Frontend directory not found (will be created later)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Node.js not found. Frontend setup skipped.${NC}"
    echo "  Install Node.js 18+ from: https://nodejs.org/"
fi
echo ""

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p ~/.package-audit/storage
mkdir -p ~/.package-audit/snapshots
mkdir -p ~/.package-audit/manifests
echo -e "${GREEN}✓ Directories created in ~/.package-audit/${NC}"
echo ""

# Success message
echo "========================================"
echo -e "${GREEN}✅ Setup completed successfully!${NC}"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Start the backend server:"
echo "   cd backend"
echo "   source .venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Access the API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "3. If frontend is available, start it with:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
