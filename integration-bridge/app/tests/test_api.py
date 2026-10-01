from fastapi.testclient import TestClient
from app.main import app
c = TestClient(app)
def test_rx_and_tooth():
    r = c.post("/api/v1/records/prescription", json={"patient_id":"P-1003","clinician":"Rao","items":[{"drug":"Paracetamol","dosage":"500mg","frequency":"TDS","duration":"3 days"}]})
    assert r.status_code == 200
    assert c.post("/api/v1/records/odontogram/update", json={"patient_id":"P-1001","tooth":8,"status":"caries"}).status_code == 200
    assert c.post("/api/v1/records/odontogram/update", json={"patient_id":"P-1001","tooth":40,"status":"caries"}).status_code == 422
