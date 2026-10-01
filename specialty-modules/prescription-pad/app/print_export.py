"""Printable / shareable prescription pad (HTML). CRM sends the link via WhatsApp."""
from html import escape

def render_pad(rx: dict, patient_name: str) -> str:
    rows = "".join(
        f"<tr><td>{escape(i['drug'])}</td><td>{escape(i['dosage'])}</td>"
        f"<td>{escape(i['frequency'])}</td><td>{escape(i['duration'])}</td></tr>" for i in rx["items"])
    return f"""<!doctype html><meta charset=utf-8><title>{rx['id']}</title>
<body style="font-family:system-ui;max-width:640px;margin:40px auto;color:#1b2333">
<h2 style="display:flex;align-items:center;gap:10px"><svg width=30 height=30 viewBox='0 0 64 64'><circle cx=32 cy=32 r=26 fill=none stroke=#2fd68f stroke-width=6 /><path d='M21 24h22M32 24v21' fill=none stroke=#1b2333 stroke-width=6 stroke-linecap=round /></svg>Trievo Records</h2><p><b>{escape(patient_name)}</b> &middot; {rx['issued_at'][:10]} &middot; {rx['id']}</p>
<table width=100% cellpadding=8 style="border-collapse:collapse" border=1>
<tr style="background:#e6f3ee"><th align=left>Drug</th><th align=left>Dosage</th><th align=left>Frequency</th><th align=left>Duration</th></tr>{rows}</table>
<p>{escape(rx.get('notes',''))}</p><p style="margin-top:48px">Dr. {escape(rx['clinician'])}</p></body>"""
