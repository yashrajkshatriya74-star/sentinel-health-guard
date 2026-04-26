from mcp.server.fastmcp import FastMCP
import json
import random
from datetime import datetime
import os

mcp = FastMCP("Sentinel-Health-Guard")

# Fake data
FAKE_NAMES = ["Patient-Alpha", "Patient-Beta", "Patient-Gamma"]
FAKE_PHONES = ["XXX-XXXX", "YYY-YYYY"]
FAKE_ADDRESSES = ["Privacy Lane", "Secure Blvd"]

LOG_PATH = "audit_log.txt"


def write_log(message: str):
    try:
        with open(LOG_PATH, "a") as f:
            f.write(f"[{datetime.now()}] {message}\n")
    except:
        pass


# ---------------- TOOLS ----------------

@mcp.tool()
def health_check() -> str:
    return "✅ Server running"


@mcp.tool()
def audit_patient_data(fhir_json: str) -> str:
    try:
        data = json.loads(fhir_json)
        findings = []

        if "name" in data:
            findings.append("⚠️ Name detected")
        if "telecom" in data:
            findings.append("⚠️ Contact detected")
        if "address" in data:
            findings.append("⚠️ Address detected")
        if "birthDate" in data:
            findings.append("⚠️ DOB detected")

        write_log(f"Audit: {list(data.keys())}")

        return "\n".join(findings) if findings else "✅ Safe data"

    except:
        return "❌ Invalid JSON"


@mcp.tool()
def mask_patient_data(fhir_json: str) -> str:
    try:
        data = json.loads(fhir_json)

        for key in ["name", "telecom", "address", "birthDate"]:
            if key in data:
                data[key] = "[REDACTED]"

        write_log("Mask applied")

        return json.dumps(data, indent=2)

    except:
        return "❌ Error"


@mcp.tool()
def synthetic_patient_data(fhir_json: str) -> str:
    try:
        data = json.loads(fhir_json)

        if "name" in data:
            data["name"] = random.choice(FAKE_NAMES)
        if "telecom" in data:
            data["telecom"] = random.choice(FAKE_PHONES)
        if "address" in data:
            data["address"] = random.choice(FAKE_ADDRESSES)

        write_log("Synthetic generated")

        return json.dumps(data, indent=2)

    except:
        return "❌ Error"


# ---------------- RUN ----------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))

    print("🚀 MCP Server running on port:", port)

    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=port
    )
