from fastapi import FastAPI
from paytm_mcp import mcp  # Import the MCP instance with all registered tools

app = FastAPI()
app.mount("/tools", mcp.sse_app())

# Optional: Health check
@app.get("/")
def root():
    return {"status": "MCP Server is running"}
