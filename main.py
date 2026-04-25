from mcp.server.fastmcp import FastMCP
import json
import random
from datetime import datetime
import os

mcp = FastMCP("Sentinel-Health-Guard")

# Fake Data
FAKE_NAMES = ["Patient-Alpha", "Patient-Beta", "Patient-Gamma"]
FAKE_PHONES = ["XXX-XXXX", "YYY-YYYY"]
FAKE_ADDRESSES = ["Privacy Lane", "Secure Blvd"]

# Safe Log Path
LOG_PATH = os.path.join(os.getcwd(), "audit_log.txt")

def write_log(message: str):
    try:
        with open(LOG_PATH, "a") as f:
            f.write(f"[{datetime.now()}] {message}\n")
    except:
        pass

# ✅ Common JSON validator
def parse_json_safe(fhir_json):
    try:
        data = json.loads(fhir_json)
        if not isinstance(data, dict):
            return None, "❌ Invalid JSON format (Expected object)"
        return data, None
    except json.JSONDecodeError:
        return None, "❌ Invalid JSON (Parse error)"


@mcp.tool()
def audit_patient_data(fhir_json: str) -> str:
    data, error = parse_json_safe(fhir_json)
    if error:
        return error

    findings = []
    risk_points = 0
    total_points = 100

    checks = [
        ("name", 30),
        ("telecom", 25),
        ("address", 20),
        ("birthDate", 10),
        ("identifier", 15),
    ]

    for field, points in checks:
        if field in data:
            findings.append(f"[RISK] {field} found")
            risk_points += points

    safe_percent = 100 - risk_points

    write_log(f"Audit done. Score: {safe_percent}%")

    if not findings:
        return f"✅ Safe Data\n📊 Score: {safe_percent}%"

    return f"⚠️ Audit Report\n📊 Score: {safe_percent}%\n" + "\n".join(findings)


@mcp.tool()
def mask_patient_data(fhir_json: str) -> str:
    data, error = parse_json_safe(fhir_json)
    if error:
        return error

    for field in ["name", "telecom", "address", "birthDate", "identifier"]:
        if field in data:
            data[field] = "[REDACTED]"

    write_log("Mask applied")

    return json.dumps(data, indent=2)


@mcp.tool()
def synthetic_patient_data(fhir_json: str) -> str:
    data, error = parse_json_safe(fhir_json)
    if error:
        return error

    if "name" in data:
        data["name"] = random.choice(FAKE_NAMES)
    if "telecom" in data:
        data["telecom"] = random.choice(FAKE_PHONES)
    if "address" in data:
        data["address"] = random.choice(FAKE_ADDRESSES)
    if "identifier" in data:
        data["identifier"] = f"SYNTH-{random.randint(1000,9999)}"

    write_log("Synthetic generated")

    return json.dumps(data, indent=2)


@mcp.tool()
def health_check() -> str:
    return "✅ Server Running"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("🚀 Server starting...")

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port
    )
