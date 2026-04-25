from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
import json
import os

mcp = FastMCP("Sentinel-Health-Guard")

app = FastAPI()


# -------- JSON SAFE PARSER --------
def parse_json(fhir_json):
    try:
        data = json.loads(fhir_json)
        if not isinstance(data, dict):
            return None, "Invalid JSON object"
        return data, None
    except:
        return None, "Invalid JSON format"


# -------- MCP TOOLS --------
@mcp.tool()
def health_check() -> str:
    return "OK"

@mcp.tool()
def audit_patient_data(fhir_json: str) -> str:
    data, err = parse_json(fhir_json)
    if err:
        return err

    if "name" in data:
        return "⚠️ Name detected"
    return "✅ Safe"


# -------- HTTP ROUTES --------
@app.get("/")
def root():
    return {"status": "Server running ✅"}


@app.get("/health")
def health():
    return {"status": "ok"}


# -------- MCP ASGI APP --------
mcp_app = mcp.asgi()   # 🔥 THIS IS THE FIX

mcp_app = mcp.asgi()
app.mount("/mcp", mcp_app)


# -------- RUN --------
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    print("🚀 Server starting...")

    uvicorn.run(app, host="0.0.0.0", port=port)
