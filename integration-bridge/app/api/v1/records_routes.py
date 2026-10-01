import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from app import vault_client
from app.core import config
from app.events.publisher import publish, EVENT_LOG
from prescription_writer import PrescriptionIn, build_prescription
from print_export import render_pad
from tooth_status_model import ToothUpdate, STATUS_CODES
from odontogram_api import apply_update
from photo_intake import quality_check
from timeline_grouping import group_timeline

router = APIRouter(prefix="/api/v1/records")
RX: dict = {}
CHARTS: dict = {}
PHOTOS: dict = {}
NOTES: dict = {}

from app.seed import load as _load_seed
_load_seed(RX, CHARTS, PHOTOS, NOTES)

def _patient(pid):
    p = vault_client.get_patient(pid)
    if not p: raise HTTPException(404, "Patient not found in Vault identity.")
    return p

@router.get("/patients")
def patients(): return vault_client.list_patients()

@router.get("/patients/{pid}/chart")
def chart(pid: str):
    p = _patient(pid)
    return {"patient": p, "notes": NOTES.get(pid, []),
            "prescriptions": [r for r in RX.values() if r["patient_id"] == pid],
            "odontogram": CHARTS.get(pid), "dermatology": group_timeline(PHOTOS.get(pid, []))}

@router.get("/meta")
def meta(): return {"tooth_status": STATUS_CODES, "events": EVENT_LOG[-20:]}

@router.post("/prescription")
def prescription(body: PrescriptionIn):
    _patient(body.patient_id)
    rx = build_prescription(body); RX[rx["id"]] = rx
    publish("trievo.records.prescription_issued", {"patient_id": rx["patient_id"], "prescription_id": rx["id"],
            "print_url": f"/api/v1/records/prescription/{rx['id']}/print"})
    return rx

@router.get("/prescription/{rid}/print", response_class=HTMLResponse)
def print_rx(rid: str):
    rx = RX.get(rid)
    if not rx: raise HTTPException(404, "Prescription not found.")
    return render_pad(rx, _patient(rx["patient_id"])["name"])

@router.post("/odontogram/update")
def odontogram(body: ToothUpdate):
    _patient(body.patient_id)
    CHARTS[body.patient_id] = apply_update(CHARTS.get(body.patient_id), body)
    publish("trievo.records.chart_updated", {"patient_id": body.patient_id, "module": "odontogram", "tooth": body.tooth})
    return CHARTS[body.patient_id]

@router.post("/dermatology/photo")
async def derm_photo(patient_id: str = Form(...), condition: str = Form(...), label: str = Form("follow-up"),
                     file: UploadFile = File(...)):
    _patient(patient_id)
    if not condition.strip(): raise HTTPException(422, "Tag the photo to a condition or procedure.")
    data = await file.read()
    ok, msg = quality_check(data)
    if not ok: raise HTTPException(422, msg)
    name = f"{uuid.uuid4().hex}.jpg"; (config.PHOTO_DIR / name).write_bytes(data)
    ph = {"id": name, "url": f"/photos/{name}", "condition": condition.strip(), "label": label,
          "taken_at": datetime.now(timezone.utc).isoformat()}
    PHOTOS.setdefault(patient_id, []).append(ph)
    publish("trievo.records.chart_updated", {"patient_id": patient_id, "module": "dermatology", "condition": ph["condition"]})
    return ph


from pydantic import BaseModel

class NoteIn(BaseModel):
    patient_id: str
    text: str
    clinician: str = ""

@router.post("/notes")
def add_note(body: NoteIn):
    _patient(body.patient_id)
    n = {"at": datetime.now(timezone.utc).isoformat()[:16].replace("T", " "), "text": body.text, "clinician": body.clinician}
    NOTES.setdefault(body.patient_id, []).append(n)
    publish("trievo.records.chart_updated", {"patient_id": body.patient_id, "module": "notes"})
    return n
