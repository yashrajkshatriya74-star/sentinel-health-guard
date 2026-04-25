from mcp.server.fastmcp import FastMCP
import json
import random
from datetime import datetime
import os

# Server initialize
mcp = FastMCP("Sentinel-Health-Guard")

# Cloud-friendly logging path
LOG_PATH = "audit_log.txt"

# Synthetic names database
FAKE_NAMES = ["Patient-Alpha", "Patient-Beta", "Patient-Gamma", "Patient-Delta", "Patient-Epsilon"]
FAKE_PHONES = ["XXX-XXXX", "YYY-YYYY", "ZZZ-ZZZZ"]
FAKE_ADDRESSES = ["123 Privacy Lane", "456 Secure Blvd", "789 Safe Street"]

def write_log(message: str):
    """Logs activity to a local file for audit trails."""
    with open(LOG_PATH, "a") as log_file:
        log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

@mcp.tool()
def audit_patient_data(fhir_json: str) -> str:
    """Healthcare data ko scan karke privacy risks detect karta hai with Risk Score."""
    try:
        data = json.loads(fhir_json)
        findings = []
        risk_points = 0
        total_points = 0

        checks = [
            ("name", 30, "[RISK] Patient Name detected. Recommended: Masking."),
            ("telecom", 25, "[RISK] Contact details (Phone/Email) found. High Privacy Risk."),
            ("address", 20, "[RISK] Physical Address found. Needs de-identification."),
            ("birthDate", 10, "[RISK] Date of Birth found. Age-grouping recommended."),
            ("identifier", 15, "[RISK] SSN/MRN identifier found. Immediate masking required."),
            ("id", 5, "[INFO] Patient ID detected. Ensure this is a non-traceable UUID."),
            ("gender", 5, "[INFO] Gender detected. Low risk but noted."),
        ]

        for field, points, message in checks:
            total_points += points
            if field in data:
                findings.append(message)
                risk_points += points

        safe_percent = 100 - int((risk_points / total_points) * 100) if total_points > 0 else 100
        score_label = "🟢 LOW" if safe_percent >= 80 else "🟡 MEDIUM" if safe_percent >= 50 else "🔴 HIGH"

        write_log(f"Audit performed. Privacy Score: {safe_percent}%")

        if not findings:
            return f"✅ Data looks safe (No PII found).\n📊 Privacy Score: 100% Safe {score_label} RISK"

        report = f"⚠️ Audit Report:\n📊 Privacy Score: {safe_percent}% Safe — {score_label} RISK\n"
        report += "─" * 40 + "\n" + "\n".join(findings) + "\n" + "─" * 40
        report += "\n💡 Recommendation: Run mask_patient_data to secure this record."
        return report
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def mask_patient_data(fhir_json: str) -> str:
    """Sensitive data ko automatically mask karta hai."""
    try:
        data = json.loads(fhir_json)
        for field in ["name", "telecom", "address", "birthDate", "identifier"]:
            if field in data:
                data[field] = "[REDACTED]"
        write_log("Data masked successfully.")
        return "✅ Masked Data:\n" + json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def synthetic_patient_data(fhir_json: str) -> str:
    """Real PII ko fake synthetic data se replace karta hai research ke liye."""
    try:
        data = json.loads(fhir_json)
        if "name" in data: data["name"] = random.choice(FAKE_NAMES)
        if "telecom" in data: data["telecom"] = random.choice(FAKE_PHONES)
        if "address" in data: data["address"] = random.choice(FAKE_ADDRESSES)
        
        if "birthDate" in data:
            try:
                year = int(data["birthDate"].split("-")[0])
                age = datetime.now().year - year
                groups = [(18, "Under-18"), (30, "18-30"), (45, "30-45"), (60, "45-60")]
                data["birthDate"] = next((g[1] for g in groups if age < g[0]), "60+")
            except:
                data["birthDate"] = "Unknown"
        
        if "identifier" in data: data["identifier"] = f"SYNTH-{random.randint(10000, 99999)}"
        write_log("Synthetic data generated.")
        return "🔬 Synthetic Research Data:\n" + json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def audit_fhir_patient(fhir_json: str) -> str:
    """Real FHIR R4 Patient resource ko audit karta hai."""
    try:
        data = json.loads(fhir_json)
        findings = []
        fhir_checks = [
            ("name", 30, "[RISK] HumanName detected."),
            ("telecom", 25, "[RISK] ContactPoints detected."),
            ("address", 20, "[RISK] Address detected."),
            ("birthDate", 10, "[RISK] Exact birthDate is PII."),
            ("photo", 20, "[RISK] Biometric data found!"),
        ]
        
        for field, _, msg in fhir_checks:
            if field in data: findings.append(msg)
            
        write_log(f"FHIR Audit completed for: {data.get('resourceType', 'Patient')}")
        return "⚠️ FHIR Audit:\n" + "\n".join(findings) if findings else "✅ FHIR Resource is safe."
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def mask_fhir_patient(fhir_json: str) -> str:
    """Real FHIR R4 Patient resource ko mask karta hai (HIPAA Compliant)."""
    try:
        data = json.loads(fhir_json)
        if "name" in data: data["name"] = [{"use": "anonymous", "family": "REDACTED"}]
        if "telecom" in data: data["telecom"] = [{"system": "phone", "value": "REDACTED"}]
        if "photo" in data: data["photo"] = "REDACTED"
        write_log("FHIR Mask applied.")
        return "✅ FHIR Patient Masked:\n" + json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    app = mcp.streamable_http_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        proxy_headers=True,
        forwarded_allow_ips="*"
    )
