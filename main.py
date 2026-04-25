from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("Sentinel-Health-Guard")

@mcp.tool()
def health_check() -> str:
    return "✅ Server running"

@mcp.tool()
def audit_patient_data(fhir_json: str) -> str:
    try:
        data = json.loads(fhir_json)

        if not isinstance(data, dict):
            return "❌ Invalid JSON object"

        findings = []

        if "name" in data:
            findings.append("⚠️ Name detected")

        if "address" in data:
            findings.append("⚠️ Address detected")

        if "telecom" in data:
            findings.append("⚠️ Contact detected")

        if not findings:
            return "✅ Safe data"

        return "\n".join(findings)

    except:
        return "❌ Invalid JSON"

if __name__ == "__main__":
    print("🚀 MCP Server starting...")
    mcp.run()
