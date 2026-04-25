from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("Sentinel-Health-Guard")

@mcp.tool()
def health_check() -> str:
    return "✅ Sentinel Health Guard is running!"

@mcp.tool()
def audit_patient_data(fhir_json: str) -> str:
    try:
        data = json.loads(fhir_json)
        findings = []
        if "name" in data: findings.append("⚠️ Name detected")
        if "telecom" in data: findings.append("⚠️ Contact detected")
        if "address" in data: findings.append("⚠️ Address detected")
        if "birthDate" in data: findings.append("⚠️ DOB detected")
        return "\n".join(findings) if findings else "✅ Safe data"
    except:
        return "❌ Invalid JSON"

if __name__ == "__main__":
    mcp.run()
