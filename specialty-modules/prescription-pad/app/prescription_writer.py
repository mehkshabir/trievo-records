"""Structured prescription builder (drug, dosage, frequency, duration, clinician)."""
import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class DrugLine(BaseModel):
    drug: str = Field(min_length=2)
    dosage: str
    frequency: str
    duration: str

class PrescriptionIn(BaseModel):
    patient_id: str
    clinician: str
    items: list[DrugLine] = Field(min_length=1)
    notes: str = ""

def build_prescription(p: PrescriptionIn) -> dict:
    return {"id": "RX-" + uuid.uuid4().hex[:8].upper(),
            "issued_at": datetime.now(timezone.utc).isoformat(),
            **p.model_dump()}
