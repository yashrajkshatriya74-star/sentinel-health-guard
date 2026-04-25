from fastapi import FastAPI
import json
import random
from datetime import datetime
import os

app = FastAPI()

FAKE_NAMES = ["Patient-Alpha", "Patient-Beta", "Patient-Gamma"]
FAKE_PHONES = ["XXX-XXXX", "YYY-YYYY"]
FAKE_ADDRESSES = ["123 Privacy Lane", "456 Secure Blvd"]

LOG_PATH = os.path.join(os.getcwd(), "audit_log.txt")


def write_log(msg):
    try:
        with open(LOG_PATH, "a") as f:
            f.write(msg + "\n")
    except:
        pass


def parse_json(data):
    if not isinstance(data, dict):
        return None, "Invalid JSON object"
    return data, None


# ---------------- ROUTES ----------------

@app.get("/")
def root():
    return {"status": "Sentinel running ✅"}


@app.post("/audit")
def audit(data: dict):
    findings = []

    if "name" in data:
        findings.append("Name detected")
    if "telecom" in data:
        findings.append("Phone detected")
    if "address" in data:
        findings.append("Address detected")

    if not findings:
        return {"result": "Safe"}

    return {"result": findings}


@app.post("/mask")
def mask(data: dict):
    for key in ["name", "telecom", "address", "birthDate", "identifier"]:
        if key in data:
            data[key] = "[REDACTED]"

    return {"masked": data}


@app.post("/synthetic")
def synthetic(data: dict):
    if "name" in data:
        data["name"] = random.choice(FAKE_NAMES)
    if "telecom" in data:
        data["telecom"] = random.choice(FAKE_PHONES)
    if "address" in data:
        data["address"] = random.choice(FAKE_ADDRESSES)

    return {"synthetic": data}


# ---------------- RUN ----------------

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
