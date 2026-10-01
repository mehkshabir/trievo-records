"""Loads dummy demo records (no images) from seed_data.json into the in-memory stores."""
import json
from pathlib import Path
from tooth_status_model import blank_chart
DATA = json.loads((Path(__file__).parent / "seed_data.json").read_text())

def load(RX, CHARTS, PHOTOS, NOTES):
    for pid, r in DATA["records"].items():
        NOTES[pid] = [{"at": a, "text": t, "clinician": c} for a, t, c in r.get("notes", [])]
        for k, (d, clin, items) in enumerate(r.get("rx", []), 1):
            rid = f"RX-{pid[2:]}{k:02d}"
            RX[rid] = {"id": rid, "patient_id": pid, "clinician": clin, "issued_at": d + "T10:00:00+00:00", "notes": "",
                       "items": [dict(drug=a, dosage=b, frequency=c, duration=e) for a, b, c, e in items]}
        if r.get("teeth"):
            ch = blank_chart()
            for n, st, note, d in r["teeth"]:
                t = ch[str(n)]; t["history"].append({"from": t["status"], "to": st, "note": note, "at": d + "T09:00:00+00:00"}); t["status"] = st
            CHARTS[pid] = ch
        if r.get("derm"):
            PHOTOS[pid] = [{"id": f"seed-{pid}-{i}", "url": None, "condition": c, "label": l, "taken_at": d + "T10:00:00+00:00"}
                           for c, a in r["derm"].items() for i, (l, d) in enumerate(a)]
