# 🛡️ Sentinel-Health-Guard

**A HIPAA-Compliant AI Privacy Guardian for Healthcare Data**

> Built for the **Agents Assemble — Healthcare AI Endgame Challenge** by Prompt Opinion & Darena Health

[![MCP Server](https://img.shields.io/badge/MCP-Server-blue)](https://modelcontextprotocol.io)
[![FHIR R4](https://img.shields.io/badge/FHIR-R4-green)](https://hl7.org/fhir/)
[![HIPAA](https://img.shields.io/badge/HIPAA-Compliant-red)](https://www.hhs.gov/hipaa)
[![Python](https://img.shields.io/badge/Python-3.11-yellow)](https://python.org)

---

## 🏥 The Problem

Doctors and researchers share sensitive patient data (FHIR format) with AI models without checking for PII (Personally Identifiable Information). This violates HIPAA regulations and puts patient privacy at risk. Healthcare organizations face millions in fines annually due to improper data handling.

## 💡 The Solution

**Sentinel-Health-Guard** is a HIPAA-compliant MCP (Model Context Protocol) server that acts as an **AI Privacy Layer** — auditing, masking, and synthesizing patient data before it reaches any AI model.

> *"Healthcare AI should be powerful AND private."*

---

## 🚀 8 Powerful Tools

### 🔍 1. `audit_patient_data`
Scans patient records and detects PII with a **Privacy Risk Score**.
- Detects: Name, Phone, Address, DOB, SSN/MRN, Gender, ID
- Returns: Risk Score (🟢 LOW / 🟡 MEDIUM / 🔴 HIGH)
- Logs every audit to `audit_log.txt` for compliance trail

### 🛡️ 2. `mask_patient_data`
Automatically replaces all sensitive fields with `[REDACTED]`.
- HIPAA-compliant output
- Safe for sharing with AI models

### 🔬 3. `synthetic_patient_data`
Replaces real PII with realistic fake data for research.
- Names → Patient-Alpha, Patient-Beta, etc.
- DOB → Age Groups (18-30, 30-45, etc.)
- Phone → XXX-XXXX format

### 🏥 4. `audit_fhir_patient`
Full FHIR R4 standard compliance check.
- Checks: HumanName, ContactPoints, Address, Biometric data, Emergency contacts
- Resource type aware (Patient, Observation, etc.)

### 🔒 5. `mask_fhir_patient`
HIPAA-compliant masking of real FHIR R4 Patient resources.
- Preserves FHIR structure
- Anonymizes identifiers with ANON-XXXXX format

### ✅ 6. `check_consent`
Verifies patient consent before data sharing.
- Checks for consent/authorization fields
- Prevents unauthorized data sharing

### 📋 7. `batch_audit`
Audit multiple patient records simultaneously.
- Processes entire patient datasets at once
- Returns summary with risk breakdown
- Identifies how many patients need immediate masking

### 📄 8. `hipaa_compliance_report`
Generates detailed HIPAA compliance reports.
- References specific HIPAA regulations (45 CFR §164.514)
- Categorizes violations as HIGH/MEDIUM/LOW risk
- Provides actionable remediation steps

---

## 📊 How It Works

```
Patient Data → Sentinel-Health-Guard → Privacy Audit → Safe AI Input
                        ↓
                   Audit Log Trail
```

1. **Audit** — Scan data for PII risks
2. **Score** — Calculate Privacy Risk Score
3. **Mask/Synthesize** — Protect sensitive data
4. **Log** — Record all operations for compliance

---

## 🛠️ Tech Stack

- **FastMCP** — Model Context Protocol server framework
- **Python 3.11** — Core language
- **FHIR R4** — Healthcare data standard
- **Claude Desktop** — Local MCP integration
- **Prompt Opinion** — Healthcare AI agent platform

---

## 📋 Installation

```bash
git clone https://github.com/yashrajkshatriya74-star/sentinel-health-guard.git
cd sentinel-health-guard
pip install -r requirements.txt
python main.py
```

---

## 🔧 Claude Desktop Integration

Add to `%AppData%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sentinel-health": {
      "command": "path/to/venv/Scripts/python.exe",
      "args": ["path/to/main.py"]
    }
  }
}
```

---

## 🧪 Example Usage

**Audit:**
```json
{"name": "John Doe", "telecom": "555-1234", "address": "123 Main St", "birthDate": "1990-01-01"}
```

**Output:**
```
⚠️ Audit Report:
📊 Privacy Score: 15% Safe — 🔴 HIGH RISK
[RISK] Patient Name detected. Recommended: Masking.
[RISK] Contact details found. High Privacy Risk.
[RISK] Physical Address found. Needs de-identification.
[RISK] Date of Birth found. Age-grouping recommended.
💡 Recommendation: Run mask_patient_data to secure this record.
```

**Batch Audit:**
```json
[
  {"name": "John Doe", "telecom": "555-1234"},
  {"name": "Jane Smith", "address": "456 Oak Ave"},
  {"id": "uuid-123"}
]
```

**HIPAA Report Output:**
```
📄 HIPAA COMPLIANCE REPORT
🚨 Violations (High Risk): 3
⚠️ Warnings (Low-Med Risk): 1
❌ NON-COMPLIANT: 3 HIPAA violations found.
💡 Run mask_patient_data to achieve compliance.
```

---

## 📊 Audit Trail

Every operation is logged:
```
[2026-04-23 09:15:32] Audit performed. Privacy Score: 15%
[2026-04-23 09:16:01] Data masked successfully.
[2026-04-23 09:16:45] Synthetic data generated.
[2026-04-23 09:17:12] HIPAA Report generated. Violations: 3
[2026-04-23 09:18:00] Batch audit performed on 3 patients.
```

---

## 🏆 Why Sentinel-Health-Guard?

| Feature | Others | Sentinel |
|---------|--------|----------|
| Privacy before AI | ❌ | ✅ |
| Risk Scoring | ❌ | ✅ |
| FHIR R4 Support | ❌ | ✅ |
| Audit Trail | ❌ | ✅ |
| Synthetic Data | ❌ | ✅ |
| Batch Processing | ❌ | ✅ |
| Consent Check | ❌ | ✅ |
| HIPAA Reports | ❌ | ✅ |
| MCP Protocol | ❌ | ✅ |

---

## 👨‍💻 Built By

**Yashraj Shivam Kshatriya** — SentinelHealth

*Agents Assemble — Healthcare AI Endgame Challenge 2026*
