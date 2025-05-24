#!/bin/bash
# Financial Risk Assessment System Startup Script
# Cross-platform launcher for Unix-like systems

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_MIN_VERSION="3.8"
VENV_DIR="$PROJECT_DIR/venv"
LOG_FILE="$PROJECT_DIR/startup.log"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║              Financial Risk Assessment System                 ║"
    echo "║                      Professional Edition                     ║"
    echo "║                         Version 2.0.0                        ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    local python_cmd=$1
    if ! command_exists "$python_cmd"; then
        return 1
    fi
    
    local version=$($python_cmd -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    local required_version="$PYTHON_MIN_VERSION"
    
    if [ "$(printf '%s\n' "$required_version" "$version" | sort -V | head -n1)" = "$required_version" ]; then
        echo "$python_cmd"
        return 0
    fi
    return 1
}

# Function to find suitable Python interpreter
find_python() {
    for python_cmd in python3 python python3.11 python3.10 python3.9 python3.8; do
        if python_exe=$(check_python_version "$python_cmd"); then
            echo "$python_exe"
            return 0
        fi
    done
    return 1
}

# Function to create virtual environment
create_venv() {
    local python_exe=$1
    
    if [ -d "$VENV_DIR" ]; then
        print_status "Virtual environment already exists"
        return 0
    fi
    
    print_status "Creating virtual environment..."
    "$python_exe" -m venv "$VENV_DIR"
    
    if [ $? -eq 0 ]; then
        print_status "Virtual environment created successfully"
        return 0
    else
        print_error "Failed to create virtual environment"
        return 1
    fi
}

# Function to activate virtual environment
activate_venv() {
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
        print_status "Virtual environment activated"
        return 0
    else
        print_warning "Virtual environment not found"
        return 1
    fi
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Upgrade pip first
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "$PROJECT_DIR/requirements.txt" ]; then
        pip install -r "$PROJECT_DIR/requirements.txt"
        if [ $? -eq 0 ]; then
            print_status "Dependencies installed successfully"
            return 0
        else
            print_error "Failed to install dependencies"
            return 1
        fi
    else
        print_warning "requirements.txt not found"
        return 1
    fi
}

# Function to check system requirements
check_system_requirements() {
    print_status "Checking system requirements..."
    
    # Check for required system packages on Linux
    if command_exists apt-get; then
        # Ubuntu/Debian
        required_packages=("python3-dev" "python3-venv" "libpq-dev" "build-essential")
        missing_packages=()
        
        for package in "${required_packages[@]}"; do
            if ! dpkg -l | grep -q "^ii  $package "; then
                missing_packages+=("$package")
            fi
        done
        
        if [ ${#missing_packages[@]} -gt 0 ]; then
            print_warning "Missing system packages: ${missing_packages[*]}"
            read -p "Install missing packages? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                sudo apt-get update
                sudo apt-get install -y "${missing_packages[@]}"
            fi
        fi
    elif command_exists yum; then
        # RHEL/CentOS
        print_warning "Please ensure python3-devel, postgresql-devel, and gcc are installed"
    elif command_exists brew; then
        # macOS
        if ! command_exists postgresql; then
            print_warning "PostgreSQL not found. Install with: brew install postgresql"
        fi
    fi
    
    # Check for X11 display (Linux)
    if [[ "$OSTYPE" == "linux-gnu"* ]] && [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
        print_warning "No display server detected. GUI may not work properly."
    fi
}

# Function to run the application
run_application() {
    local mode=${1:-gui}
    local command=$2
    
    cd "$PROJECT_DIR/project code"
    
    case $mode in
        gui)
            print_status "Starting GUI application..."
            python run.py --mode gui
            ;;
        api)
            print_status "Starting API server..."
            python run.py --mode api
            ;;
        cli)
            if [ -n "$command" ]; then
                print_status "Running CLI command: $command"
                python run.py --mode cli --command "$command"
            else
                print_error "CLI mode requires a command"
                return 1
            fi
            ;;
        test)
            print_status "Running tests..."
            python run.py --mode cli --command test
            ;;
        *)
            print_error "Unknown mode: $mode"
            return 1
            ;;
    esac
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] [MODE] [COMMAND]"
    echo ""
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  -v, --verbose           Verbose output"
    echo "  --check-only            Only check system requirements"
    echo "  --setup-only            Only setup environment"
    echo "  --no-venv               Don't use virtual environment"
    echo ""
    echo "Modes:"
    echo "  gui                     Launch GUI application (default)"
    echo "  api                     Launch API server"
    echo "  cli COMMAND             Run CLI command"
    echo "  test                    Run test suite"
    echo ""
    echo "Examples:"
    echo "  $0                      # Launch GUI"
    echo "  $0 api                  # Launch API server"
    echo "  $0 cli migrate          # Run database migration"
    echo "  $0 test                 # Run tests"
    echo "  $0 --setup-only         # Just setup environment"
}

# Main function
main() {
    local mode="gui"
    local command=""
    local check_only=false
    local setup_only=false
    local use_venv=true
    local verbose=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            --check-only)
                check_only=true
                shift
                ;;
            --setup-only)
                setup_only=true
                shift
                ;;
            --no-venv)
                use_venv=false
                shift
                ;;
            gui|api|test)
                mode=$1
                shift
                ;;
            cli)
                mode=$1
                command=$2
                shift 2
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Start logging
    exec > >(tee -a "$LOG_FILE")
    exec 2>&1
    
    print_header
    
    # System checks
    check_system_requirements
    
    # Find Python
    print_status "Looking for Python interpreter..."
    if python_exe=$(find_python); then
        print_status "Found Python: $python_exe"
    else
        print_error "Python $PYTHON_MIN_VERSION or higher not found"
        exit 1
    fi
    
    # Setup virtual environment if requested
    if [ "$use_venv" = true ]; then
        if ! create_venv "$python_exe"; then
            print_error "Failed to create virtual environment"
            exit 1
        fi
        
        if ! activate_venv; then
            print_warning "Proceeding without virtual environment"
            use_venv=false
        else
            # Install dependencies in venv
            if ! install_dependencies; then
                print_error "Failed to install dependencies"
                exit 1
            fi
        fi
    fi
    
    # Install dependencies if not using venv
    if [ "$use_venv" = false ]; then
        print_status "Installing dependencies globally..."
        "$python_exe" -m pip install --user -r "$PROJECT_DIR/requirements.txt"
    fi
    
    # Exit if only checking or setting up
    if [ "$check_only" = true ]; then
        print_status "System check completed"
        exit 0
    fi
    
    if [ "$setup_only" = true ]; then
        print_status "Environment setup completed"
        exit 0
    fi
    
    # Run the application
    if ! run_application "$mode" "$command"; then
        print_error "Application failed to start"
        exit 1
    fi
}

# Trap to handle cleanup
cleanup() {
    print_status "Cleaning up..."
    # Add any cleanup tasks here
}

trap cleanup EXIT

# Run main function
main "$@" 