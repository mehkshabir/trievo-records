"""Shared patient identity lives in Vault. Falls back to a seeded local directory for demos."""
import httpx
from app.core import config

import json
from pathlib import Path
_LOCAL = {p["id"]: p for p in json.loads((Path(__file__).parent / "seed_data.json").read_text())["patients"]}

def list_patients():
    if config.VAULT_URL:
        return httpx.get(f"{config.VAULT_URL}/api/v1/identity", timeout=5).json()
    return list(_LOCAL.values())

def get_patient(pid: str):
    if config.VAULT_URL:
        r = httpx.get(f"{config.VAULT_URL}/api/v1/identity/{pid}", timeout=5)
        return r.json() if r.status_code == 200 else None
    return _LOCAL.get(pid)
