from fastapi import FastAPI
from paytm_mcp import mcp  # ✅ IMPORT — do NOT re-instantiate MCP here

import paytm_mcp

app = FastAPI()

# ✅ Mount registered tools
app.mount("/tools", mcp.sse_app())

# ✅ Optional: health check
@app.get("/")
def root():
    return {"status": "MCP Server is running"}
