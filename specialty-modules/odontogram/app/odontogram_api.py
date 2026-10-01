from datetime import datetime, timezone
from tooth_status_model import ToothUpdate, blank_chart

def apply_update(chart, u: ToothUpdate) -> dict:
    chart = chart or blank_chart()
    t = chart[str(u.tooth)]
    t["history"].append({"from": t["status"], "to": u.status, "note": u.note,
                         "at": datetime.now(timezone.utc).isoformat()})
    t["status"] = u.status
    return chart
