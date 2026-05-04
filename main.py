from mcp.server.fastmcp import FastMCP
import json, random, os
from datetime import datetime

mcp = FastMCP("Sentinel-Health-Guard")

FAKE_NAMES = ["Patient-Alpha", "Patient-Beta", "Patient-Gamma"]
FAKE_PHONES = ["XXX-XXXX", "YYY-YYYY"]
FAKE_ADDRESSES = ["123 Privacy Lane", "456 Secure Blvd"]
LOG_PATH = "audit_log.txt"

def write_log(message):
    try:
        with open(LOG_PATH, "a") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    except: pass

@mcp.tool()
def audit_patient_data(fhir_json: str) -> str:
    """Scans patient data for PII and returns privacy risk score."""
    try:
        data = json.loads(fhir_json)
        findings = []
        risk_points = 0
        checks = [("name",30,"[RISK] Name detected."),("telecom",25,"[RISK] Phone/Email found."),("address",20,"[RISK] Address found."),("birthDate",10,"[RISK] DOB found."),("identifier",15,"[RISK] SSN/MRN found.")]
        total = sum(c[1] for c in checks)
        for field, points, msg in checks:
            if field in data:
                findings.append(msg)
                risk_points += points
        safe = 100 - int((risk_points/total)*100) if total > 0 else 100
        label = "🟢 LOW" if safe>=80 else "🟡 MEDIUM" if safe>=50 else "🔴 HIGH"
        write_log(f"Audit. Score: {safe}%")
        if not findings: return f"✅ Safe! Privacy Score: 100% {label} RISK"
        return f"⚠️ Audit:\n📊 {safe}% Safe — {label} RISK\n" + "\n".join(findings)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def mask_patient_data(fhir_json: str) -> str:
    """Masks all sensitive PII fields."""
    try:
        data = json.loads(fhir_json)
        for f in ["name","telecom","address","birthDate","identifier"]:
            if f in data: data[f] = "[REDACTED]"
        write_log("Data masked.")
        return "✅ Masked:\n" + json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def health_check() -> str:
    """Returns server status."""
    return "✅ Sentinel-Health-Guard is running!"

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 10000))
    app = mcp.sse_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        proxy_headers=True,
        forwarded_allow_ips="*",
        server_header=False
    )
