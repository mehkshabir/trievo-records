import os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
for m in ("prescription-pad", "odontogram", "dermatology-timeline"):
    sys.path.insert(0, str(ROOT / "specialty-modules" / m / "app"))
REDIS_URL = os.getenv("REDIS_URL", "")
VAULT_URL = os.getenv("VAULT_URL", "")
PHOTO_DIR = Path(os.getenv("PHOTO_DIR", ROOT / "data" / "photos")); PHOTO_DIR.mkdir(parents=True, exist_ok=True)
FRONTEND_DIR = ROOT / "frontend"
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
