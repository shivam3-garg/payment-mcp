# Paytm MCP Server

A Python-based MCP (Merchant Control Panel) server for managing Paytm payment links and transactions.

## Features

- Create Paytm payment links for customers
- Fetch all created payment links
- Retrieve transactions for a specific payment link

## Prerequisites

- Python 3.12 or higher
- Paytm Merchant credentials:
  - `PAYTM_MID`
  - `PAYTM_KEY_SECRET`
- The following Python dependencies:
  - httpx>=0.28.1
  - mcp[cli]>=1.7.0
  - paytmchecksum
  - pycryptodome
  - requests
- [uv](https://github.com/astral-sh/uv) (a fast Python package installer and runner)
- [Claude Desktop](https://www.anthropic.com/claude) (for running and managing the server)

## Installation

### Option 1: Automated Setup (Recommended)

Use the provided `setup.sh` script for automated installation and configuration:

```bash
# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

The script will:

1. Check for required dependencies (Python 3.12+, uv, Claude Desktop)
2. Clone or update the repository
3. Create and activate a virtual environment
4. Install all required dependencies
5. Create a `.env` file template for Paytm credentials

### Option 2: Manual Installation

1. **Clone the repository:**

   ```bash
   git clone git@bitbucket.org:paytmteam/payment-mcp.git
   cd payment-mcp
   ```

2. **Create and activate a virtual environment:**

   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   uv pip install .
   ```

## Configuration

1. **Create a `.env` file in the project root:**

   ```bash
   # Paytm credentials
   PAYTM_MID=your_paytm_mid
   PAYTM_KEY_SECRET=your_paytm_key_secret
   ```

2. **Update the `.env` file with your actual Paytm credentials**

## Running the MCP Server with Claude Desktop

The server is designed to be managed and run via Claude Desktop. You do not need to run the server manually from the command line.

### Sample `claude_desktop_config.json`

Place this file in your project root or as required by Claude Desktop:

```json
{
  "mcpServers": {
    "paytm-mcp-server": {
      "command": "uv path",
      "args": ["--directory", "path to project", "run", "paytm_mcp.py"],
      "env": {
        "PAYTM_MID": "****************",
        "PAYTM_KEY_SECRET": "************"
      }
    }
  }
}
```

- Update the `command` and `args` paths as needed for your environment.
- The `env` section should contain your actual Paytm credentials.

## Next Steps

1. Update the `claude_desktop_config.json` with your Paytm credentials
2. Restart the server using Claude Desktop

## Project Structure

- `paytm_mcp.py`: Main server entry point and tool definitions
- `services/`: Business logic for payments
- `config/`: Configuration and settings
- `utils/`: Data models and utilities

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License is a permissive license that allows you to:

- Use the code commercially
- Modify the code
- Distribute the code
- Use the code privately
- Sublicense the code

The only requirement is that the license and copyright notice must be included in all copies or substantial portions of the software.
