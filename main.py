from flask import Flask, request, jsonify
import json
import random
from datetime import datetime
import os

app = Flask(__name__)

FAKE_NAMES = ["Patient-Alpha", "Patient-Beta", "Patient-Gamma", "Patient-Delta"]
FAKE_PHONES = ["XXX-XXXX", "YYY-YYYY", "ZZZ-ZZZZ"]
FAKE_ADDRESSES = ["123 Privacy Lane", "456 Secure Blvd", "789 Safe Street"]

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "server": "Sentinel-Health-Guard"})

@app.route('/audit', methods=['POST'])
def audit():
    data = request.json
    findings = []
    if "name" in data: findings.append("[RISK] Patient Name detected.")
    if "telecom" in data: findings.append("[RISK] Contact details found.")
    if "address" in data: findings.append("[RISK] Physical Address found.")
    if "birthDate" in data: findings.append("[RISK] Date of Birth found.")
    return jsonify({"findings": findings, "safe": len(findings) == 0})

@app.route('/mask', methods=['POST'])
def mask():
    data = request.json
    for field in ["name", "telecom", "address", "birthDate", "identifier"]:
        if field in data:
            data[field] = "[REDACTED]"
    return jsonify({"masked_data": data})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
