#!/bin/bash
# LinkedIn Post Generator - Launch Script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   LinkedIn Post Generator - Launch Script    ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════╝${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check for .env file
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from template...${NC}"
    cat > .env << 'EOF'
# LinkedIn Post Generator Configuration

# OpenAI (required for OpenAI models)
OPENAI_API_KEY=your-openai-api-key-here

# AWS (uses default credentials from ~/.aws/credentials or IAM role)
AWS_REGION=us-east-1

# Debug mode
DEBUG=true

# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:8000
EOF
    echo -e "${GREEN}✅ Created .env file. Please edit it with your API keys.${NC}"
    echo ""
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python: $PYTHON_VERSION${NC}"

# Check/create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Install/upgrade dependencies
echo -e "${YELLOW}📥 Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Parse arguments
BACKEND_ONLY=false
FRONTEND_ONLY=false
DEV_MODE=true

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --backend) BACKEND_ONLY=true ;;
        --frontend) FRONTEND_ONLY=true ;;
        --prod) DEV_MODE=false ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --backend    Run backend only"
            echo "  --frontend   Run frontend only"
            echo "  --prod       Production mode (no hot reload)"
            echo "  -h, --help   Show this help"
            exit 0
            ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Start backend
if [ "$FRONTEND_ONLY" = false ]; then
    echo ""
    echo -e "${BLUE}🚀 Starting Backend API...${NC}"

    if [ "$DEV_MODE" = true ]; then
        uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
        BACKEND_PID=$!
        echo -e "${GREEN}✅ Backend running on http://localhost:8000 (PID: $BACKEND_PID)${NC}"
        echo -e "${GREEN}   📚 API Docs: http://localhost:8000/docs${NC}"
    else
        uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4 &
        BACKEND_PID=$!
        echo -e "${GREEN}✅ Backend running on http://localhost:8000 (Production, PID: $BACKEND_PID)${NC}"
    fi
fi

# Start frontend
if [ "$BACKEND_ONLY" = false ] && [ -d "frontend" ]; then
    echo ""
    echo -e "${BLUE}🚀 Starting Frontend...${NC}"

    cd frontend

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}📥 Installing frontend dependencies...${NC}"
        npm install
    fi

    if [ "$DEV_MODE" = true ]; then
        npm run dev &
        FRONTEND_PID=$!
        echo -e "${GREEN}✅ Frontend running on http://localhost:5173 (PID: $FRONTEND_PID)${NC}"
    else
        npm run build
        npm run preview &
        FRONTEND_PID=$!
        echo -e "${GREEN}✅ Frontend running on http://localhost:4173 (Production, PID: $FRONTEND_PID)${NC}"
    fi

    cd ..
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  All services started! Press Ctrl+C to stop.${NC}"
echo -e "${GREEN}════════════════════════════════════════════════${NC}"
echo ""

# Wait for interrupt
trap "echo ''; echo -e '${YELLOW}Shutting down...${NC}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM

# Keep script running
wait

