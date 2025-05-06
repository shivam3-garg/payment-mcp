#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.12 or higher is installed
python_version=$(python3 --version 2>&1 | awk '{print $2}')
if [[ $(echo "$python_version 3.12" | awk '{print ($1 >= $2)}') -eq 0 ]]; then
    print_error "Python 3.12 or higher is required. Current version: $python_version"
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    print_error "uv is not installed. Please install it first from https://github.com/astral-sh/uv"
    exit 1
fi

# Check if Claude Desktop is installed
if ! command -v claude &> /dev/null; then
    print_message "Claude Desktop is not installed. Please install it from https://claude.ai/download"
fi

# Create project directory
PROJECT_DIR="payment-mcp"
if [ -d "$PROJECT_DIR" ]; then
    print_message "Project directory already exists. Updating..."
    cd "$PROJECT_DIR"
    git pull
else
    print_message "Cloning repository..."
    git clone git@bitbucket.org:paytmteam/payment-mcp.git "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

# Create and activate virtual environment
print_message "Creating virtual environment..."
uv venv
source .venv/bin/activate

# Install dependencies
print_message "Installing dependencies..."
#uv pip install httpx>=0.28.1 mcp[cli]>=1.7.0 paytmchecksum pycryptodome requests
uv pip install .

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_message "Creating .env file..."
    echo "# Paytm credentials" > .env
    echo "PAYTM_MID=your_paytm_mid" >> .env
    echo "PAYTM_KEY_SECRET=your_paytm_key_secret" >> .env
    print_message "Please update the .env file with your actual Paytm credentials"
fi

print_message "Setup completed successfully!"
print_message "Next steps:"
print_message "1. Update the claude_desktop_config.json with your Paytm credentials"
print_message "2. ReStart the server using Claude Desktop" 