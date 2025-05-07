from fastapi import FastAPI
import paytm_mcp  # This forces execution of decorators
from paytm_mcp import mcp  # ✅ Import same instance that has all the tools

app = FastAPI()

# ✅ Mount MCP's sse_app under /tools
app.mount("/tools", mcp.sse_app())

@app.get("/")
def root():
    return {"status": "MCP Server is running"}
