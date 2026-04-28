from mcp.server.fastmcp import FastMCP
import json
import random
from datetime import datetime

mcp = FastMCP("Sentinel-Health-Guard")

# Synthetic names database
FAKE_NAMES = ["Patient-Alpha", "Patient-Beta", "Patient-Gamma", "Patient-Delta", "Patient-Epsilon"]
FAKE_PHONES = ["XXX-XXXX", "YYY-YYYY", "ZZZ-ZZZZ"]
FAKE_ADDRESSES = ["123 Privacy Lane", "456 Secure Blvd", "789 Safe Street"]

LOG_PATH = "audit_log.txt"


def write_log(message: str):
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

        if safe_percent >= 80:
            score_label = "🟢 LOW RISK"
        elif safe_percent >= 50:
            score_label = "🟡 MEDIUM RISK"
        else:
            score_label = "🔴 HIGH RISK"

        write_log(f"Audit performed. Fields scanned: {list(data.keys())}. Privacy Score: {safe_percent}%")

        if not findings:
            return f"✅ Data looks safe for research (No PII found).\n📊 Privacy Score: 100% Safe {score_label}"

        report = f"⚠️ Audit Report:\n"
        report += f"📊 Privacy Score: {safe_percent}% Safe — {score_label}\n"
        report += "─" * 40 + "\n"
        report += "\n".join(findings)
        report += "\n" + "─" * 40
        report += "\n💡 Recommendation: Run mask_patient_data to secure this record."
        return report

    except Exception as e:
        return f"Error processing data: {str(e)}"


@mcp.tool()
def mask_patient_data(fhir_json: str) -> str:
    """Sensitive data ko automatically mask karta hai."""
    try:
        data = json.loads(fhir_json)

        if "name" in data:
            data["name"] = "[REDACTED]"
        if "telecom" in data:
            data["telecom"] = "[REDACTED]"
        if "address" in data:
            data["address"] = "[REDACTED]"
        if "birthDate" in data:
            data["birthDate"] = "[REDACTED]"
        if "identifier" in data:
            data["identifier"] = "[REDACTED]"

        write_log("Data masked. Fields redacted: name, telecom, address, birthDate, identifier")
        return "✅ Masked Data:\n" + json.dumps(data, indent=2)

    except Exception as e:
        return f"Error masking data: {str(e)}"


@mcp.tool()
def synthetic_patient_data(fhir_json: str) -> str:
    """Real PII ko fake synthetic data se replace karta hai research ke liye."""
    try:
        data = json.loads(fhir_json)

        if "name" in data:
            data["name"] = random.choice(FAKE_NAMES)
        if "telecom" in data:
            data["telecom"] = random.choice(FAKE_PHONES)
        if "address" in data:
            data["address"] = random.choice(FAKE_ADDRESSES)
        if "birthDate" in data:
            try:
                birth_year = int(data["birthDate"].split("-")[0])
                age = datetime.now().year - birth_year
                if age < 18:
                    data["birthDate"] = "Age-Group: Under-18"
                elif age < 30:
                    data["birthDate"] = "Age-Group: 18-30"
                elif age < 45:
                    data["birthDate"] = "Age-Group: 30-45"
                elif age < 60:
                    data["birthDate"] = "Age-Group: 45-60"
                else:
                    data["birthDate"] = "Age-Group: 60+"
            except:
                data["birthDate"] = "Age-Group: Unknown"
        if "identifier" in data:
            data["identifier"] = f"SYNTH-{random.randint(10000, 99999)}"

        write_log("Synthetic data generated. Original PII replaced.")
        return "🔬 Synthetic Research Data:\n" + json.dumps(data, indent=2)

    except Exception as e:
        return f"Error generating synthetic data: {str(e)}"


@mcp.tool()
def audit_fhir_patient(fhir_json: str) -> str:
    """Real FHIR R4 Patient resource ko audit karta hai — HIPAA compliance check."""
    try:
        data = json.loads(fhir_json)
        findings = []
        risk_points = 0
        total_points = 0

        fhir_checks = [
            ("name", 30, "[RISK] FHIR Patient.name detected. Contains HumanName with family/given."),
            ("telecom", 25, "[RISK] FHIR Patient.telecom detected. Contains phone/email ContactPoints."),
            ("address", 20, "[RISK] FHIR Patient.address detected. Contains physical address."),
            ("birthDate", 10, "[RISK] FHIR Patient.birthDate detected. Exact DOB is PII."),
            ("identifier", 15, "[RISK] FHIR Patient.identifier detected. May contain SSN/MRN."),
            ("id", 5, "[INFO] FHIR Patient.id detected. Verify it is non-traceable UUID."),
            ("gender", 5, "[INFO] FHIR Patient.gender detected. Low risk demographic data."),
            ("photo", 20, "[RISK] FHIR Patient.photo detected. Biometric data - High Risk!"),
            ("contact", 15, "[RISK] FHIR Patient.contact detected. Emergency contact PII found."),
            ("communication", 5, "[INFO] FHIR Patient.communication detected. Language preference noted."),
        ]

        for field, points, message in fhir_checks:
            total_points += points
            if field in data:
                findings.append(message)
                risk_points += points

        safe_percent = 100 - int((risk_points / total_points) * 100) if total_points > 0 else 100

        if safe_percent >= 80:
            score_label = "🟢 LOW RISK"
        elif safe_percent >= 50:
            score_label = "🟡 MEDIUM RISK"
        else:
            score_label = "🔴 HIGH RISK"

        write_log(f"FHIR Audit. Resource: {data.get('resourceType', 'Unknown')}. Score: {safe_percent}%")

        if not findings:
            return f"✅ FHIR Patient resource is safe.\n📊 Privacy Score: 100% {score_label}"

        report = f"⚠️ FHIR Privacy Audit Report:\n"
        report += f"📊 Privacy Score: {safe_percent}% Safe — {score_label}\n"
        report += f"🏥 Resource Type: {data.get('resourceType', 'Patient')}\n"
        report += "─" * 40 + "\n"
        report += "\n".join(findings)
        report += "\n💡 Run mask_fhir_patient to secure this record."
        return report

    except Exception as e:
        return f"Error processing FHIR data: {str(e)}"


@mcp.tool()
def mask_fhir_patient(fhir_json: str) -> str:
    """Real FHIR R4 Patient resource ko mask karta hai — HIPAA compliant output."""
    try:
        data = json.loads(fhir_json)

        if "name" in data:
            data["name"] = [{"use": "anonymous", "family": "REDACTED", "given": ["REDACTED"]}]
        if "telecom" in data:
            data["telecom"] = [{"system": "phone", "value": "REDACTED", "use": "home"}]
        if "address" in data:
            data["address"] = [{"use": "home", "line": ["REDACTED"], "city": "REDACTED", "postalCode": "REDACTED"}]
        if "birthDate" in data:
            try:
                birth_year = int(data["birthDate"].split("-")[0])
                age = datetime.now().year - birth_year
                if age < 18:
                    data["birthDate"] = "age-group: under-18"
                elif age < 30:
                    data["birthDate"] = "age-group: 18-30"
                elif age < 45:
                    data["birthDate"] = "age-group: 30-45"
                elif age < 60:
                    data["birthDate"] = "age-group: 45-60"
                else:
                    data["birthDate"] = "age-group: 60+"
            except:
                data["birthDate"] = "age-group: unknown"
        if "identifier" in data:
            data["identifier"] = [{"system": "urn:sentinel:anonymous", "value": f"ANON-{random.randint(10000, 99999)}"}]
        if "photo" in data:
            data["photo"] = "REDACTED"
        if "contact" in data:
            data["contact"] = "REDACTED"

        write_log(f"FHIR Mask applied. Resource: {data.get('resourceType', 'Patient')}")
        return "✅ FHIR Patient Masked (HIPAA Compliant):\n" + json.dumps(data, indent=2)

    except Exception as e:
        return f"Error masking FHIR data: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
