# Trievo Records
Multi-specialty EMR layer: prescription pad, 32-tooth odontogram, dermatology photo timeline, on top of OpenEMR.
One container serves the dashboard (`frontend/`) and the API (`integration-bridge/`).

## Layout
    frontend/              dashboard (HTML/CSS/JS, logo in assets/)
    integration-bridge/    FastAPI backend, events, Vault client, seed data
    specialty-modules/     prescription-pad, odontogram, dermatology-timeline
    openemr-config/        optional OpenEMR deployment
    Dockerfile, docker-compose.yml, .env.example

## Deploy
**Docker (any VPS):** `docker compose up -d --build`, then open http://SERVER:8000
**Render / Railway / Fly / Cloud Run:** point at this repo, choose "Dockerfile". The app listens on `$PORT`. Mount a persistent disk at `/data/photos`. Health check: `/health`.
**Without Docker:**
    cd integration-bridge && pip install -r requirements.txt
    PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000

## Before real patients
- Charts, prescriptions and notes are held in memory (demo data loads from `integration-bridge/app/seed_data.json`). Wire persistence to OpenEMR before clinical use.
- Add authentication and HTTPS (reverse proxy such as Caddy or Nginx). The API has no login yet.
- Set `VAULT_URL` to use real shared patient identity instead of the demo patients.
- Dermatology photos are stored on disk at `PHOTO_DIR`; swap to MinIO for object storage.

## API
POST /api/v1/records/prescription | odontogram/update | dermatology/photo | notes
Events (Redis Streams when REDIS_URL set): trievo.records.prescription_issued, trievo.records.chart_updated
Tests: `cd integration-bridge && PYTHONPATH=. pytest`
