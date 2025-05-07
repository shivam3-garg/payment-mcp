from fastapi import FastAPI
from paytm_mcp import mcp  # ✅ Import same instance that has all the tools

app = FastAPI()

# ✅ Mount MCP's sse_app under /tools
app.mount("/tools", mcp.sse_app())

@app.get("/")
def root():
    return {"status": "MCP Server is running"}
