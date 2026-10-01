"""Standard adult 32-tooth chart (Universal numbering 1-32) with clinician-recognised status codes."""
from pydantic import BaseModel, field_validator

STATUS_CODES = {"healthy": "Healthy", "caries": "Caries", "filled": "Filled", "missing": "Missing",
                "crowned": "Crowned", "root_canal": "Root canal", "implant": "Implant",
                "extraction_planned": "Extraction planned"}

class ToothUpdate(BaseModel):
    patient_id: str
    tooth: int
    status: str
    note: str = ""
    @field_validator("tooth")
    @classmethod
    def _t(cls, v):
        if not 1 <= v <= 32: raise ValueError("tooth must be 1-32")
        return v
    @field_validator("status")
    @classmethod
    def _s(cls, v):
        if v not in STATUS_CODES: raise ValueError(f"status must be one of {list(STATUS_CODES)}")
        return v

def blank_chart() -> dict:
    return {str(n): {"status": "healthy", "history": []} for n in range(1, 33)}
