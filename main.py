from fastapi import FastAPI
from paytm_mcp import mcp  # Import the MCP instance with all registered tools

app = FastAPI()
app.mount("/", mcp.asgi_app())# Mounts the MCP server at `/tools` and `/tool/...`

# Optional: Health check
@app.get("/")
def root():
    return {"status": "MCP Server is running"}
