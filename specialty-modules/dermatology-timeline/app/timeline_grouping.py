"""Explicit grouping: photos belong together only if the clinician tagged the same condition."""
from collections import defaultdict

def group_timeline(photos: list) -> dict:
    groups = defaultdict(list)
    for p in sorted(photos, key=lambda x: x["taken_at"]):
        groups[p["condition"]].append(p)
    return dict(groups)
