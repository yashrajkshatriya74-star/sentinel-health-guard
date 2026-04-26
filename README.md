# 🛡️ Sentinel-Health-Guard

**A HIPAA-Compliant AI Privacy Guardian for Healthcare Data**

> Built for the **Agents Assemble — Healthcare AI Endgame Challenge** by Prompt Opinion & Darena Health

---

## 🏥 Problem

Doctors and researchers share patient data (FHIR format) with AI models without checking for sensitive PII (Personally Identifiable Information). This violates HIPAA regulations and puts patient privacy at risk.

## 💡 Solution

**Sentinel-Health-Guard** is an MCP (Model Context Protocol) server that acts as a **privacy layer between patient data and AI models**. Before any data reaches an AI, Sentinel audits it, scores its risk level, masks sensitive fields, and generates synthetic safe alternatives for research.

---

## 🚀 Features

### 🔍 1. Audit Patient Data
Scans FHIR patient records and detects PII with a **Privacy Risk Score**.
- Detects: Name, Phone, Address, DOB, SSN/MRN, Gender
- Returns: Risk Score (🟢 LOW / 🟡 MEDIUM / 🔴 HIGH)
- Logs: Every audit to `audit_log.txt` for compliance trail

### 🛡️ 2. Mask Patient Data
Automatically replaces all sensitive fields with `[REDACTED]`.
- HIPAA-compliant output
- Safe for sharing with AI models

### 🔬 3. Synthetic Data Generator
Replaces real PII with realistic fake data for research purposes.
- Names → Patient-Alpha, Patient-Beta, etc.
- DOB → Age Groups (18-30, 30-45, etc.)
- Phone → XXX-XXXX format

### 🏥 4. FHIR R4 Audit
Full FHIR R4 standard compliance check.
- Checks: HumanName, ContactPoints, Address, Biometric data
- Resource type aware

### 🔒 5. FHIR R4 Masking
HIPAA-compliant masking of real FHIR R4 Patient resources.
- Preserves FHIR structure
- Anonymizes identifiers with ANON-XXXXX format

---

## 🛠️ Tech Stack

- **MCP Protocol** — Model Context Protocol (FastMCP)
- **Python 3.11**
- **FHIR R4** — Healthcare data standard
- **Claude Desktop** — Local MCP integration
- **Prompt Opinion** — Healthcare AI platform

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

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sentinel-health": {
      "command": "python",
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
```

---

## 📊 Audit Trail

Every operation is logged to `audit_log.txt`:
```
[2026-04-23 09:15:32] Audit performed. Privacy Score: 15%
[2026-04-23 09:16:01] Data masked successfully.
[2026-04-23 09:16:45] Synthetic data generated.
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
| MCP Protocol | ❌ | ✅ |

---

## 👨‍💻 Built By

**Yashraj Shivam Kshatriya** — SentinelHealth

*"Healthcare AI should be powerful AND private."*
