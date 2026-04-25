from fastapi import FastAPI
import json

app = FastAPI()

def parse_json(fhir_json):
    try:
        data = json.loads(fhir_json)
        if not isinstance(data, dict):
            return None, "Invalid JSON object"
        return data, None
    except:
        return None, "Invalid JSON format"

@app.get("/")
def root():
    return {"status": "Server running ✅"}

@app.post("/audit")
def audit(data: dict):
    if "name" in data:
        return {"result": "⚠️ Name detected"}
    return {"result": "✅ Safe"}
