#!/bin/bash

# 3D AR Demo Project Setup Script
# This script sets up the development environment for the 3D AR demo project

set -e  # Exit on any error

echo "🚀 Setting up 3D AR Demo Project..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.8+ is installed
check_python() {
    print_status "Checking Python version..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python3"
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            exit 1
        fi
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python"
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python not found. Please install Python 3.8+"
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        print_success "pip found"
        PIP_CMD="pip"
    else
        print_error "pip not found. Please install pip"
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    $PIP_CMD install --upgrade pip
    $PIP_CMD install -r requirements.txt
    print_success "Dependencies installed"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    # Create data directories
    mkdir -p data/generated_models/{glb,usdz,obj,metadata}
    mkdir -p data/cache/{downloads,conversions}
    mkdir -p data/logs
    
    # Create config directory if it doesn't exist
    mkdir -p config
    
    # Create __init__.py files for Python packages
    find src -type d -exec touch {}/__init__.py \;
    touch config/__init__.py
    touch tests/__init__.py
    
    print_success "Directories created"
}

# Set up environment file
setup_env() {
    print_status "Setting up environment configuration..."
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_success "Environment file created from template"
            print_warning "Please edit .env file with your API keys and configuration"
        else
            print_warning "No .env.example found. Creating basic .env file..."
            cat > .env << EOF
# Tripo AI API Configuration
TRIPO_API_KEY=your_tripo_api_key_here
TRIPO_API_URL=https://api.tripo.ai

# MCP Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000

# Web Server Configuration
WEB_SERVER_HOST=localhost
WEB_SERVER_PORT=5000
DEBUG=True

# File Storage
MODEL_STORAGE_PATH=./data/generated_models
CACHE_PATH=./data/cache
LOG_PATH=./data/logs

# Database Configuration
DATABASE_URL=sqlite:///./data/app.db

# Redis Configuration (for caching and background tasks)
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your_secret_key_here
EOF
            print_success "Basic environment file created"
            print_warning "Please edit .env file with your actual API keys and configuration"
        fi
    else
        print_warning "Environment file already exists"
    fi
}

# Set up pre-commit hooks
setup_pre_commit() {
    print_status "Setting up pre-commit hooks..."
    if command -v pre-commit &> /dev/null; then
        pre-commit install
        print_success "Pre-commit hooks installed"
    else
        print_warning "pre-commit not found. Install with: pip install pre-commit"
    fi
}

# Run initial tests
run_tests() {
    print_status "Running initial tests..."
    if command -v pytest &> /dev/null; then
        pytest tests/ -v --tb=short
        print_success "Tests completed"
    else
        print_warning "pytest not found. Tests will be skipped"
    fi
}

# Create .gitignore if it doesn't exist
create_gitignore() {
    if [ ! -f ".gitignore" ]; then
        print_status "Creating .gitignore file..."
        cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/

# Environment Variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite
*.sqlite3

# Cache
.cache/
cache/
*.cache

# Generated Models
data/generated_models/
data/cache/

# Coverage
.coverage
htmlcov/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Celery
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# Temporary files
*.tmp
*.temp
EOF
        print_success ".gitignore file created"
    fi
}

# Main setup function
main() {
    print_status "Starting 3D AR Demo Project setup..."
    
    check_python
    check_pip
    create_venv
    activate_venv
    install_dependencies
    create_directories
    setup_env
    create_gitignore
    setup_pre_commit
    run_tests
    
    print_success "Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file with your API keys and configuration"
    echo "2. Start the MCP server: python scripts/start_mcp_server.py"
    echo "3. Start the web server: python scripts/start_web_server.py"
    echo "4. Open http://localhost:5000 in your browser"
    echo ""
    echo "For more information, see the README.md file"
}

# Run main function
main "$@" 