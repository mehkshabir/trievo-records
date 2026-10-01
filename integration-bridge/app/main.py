from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core import config
from app.api.v1.records_routes import router

app = FastAPI(title="Trievo Records Integration Bridge")
app.add_middleware(CORSMiddleware, allow_origins=config.CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.get("/health")
def health(): return {"status": "ok", "service": "trievo-records"}

app.mount("/photos", StaticFiles(directory=config.PHOTO_DIR), name="photos")
app.mount("/", StaticFiles(directory=config.FRONTEND_DIR, html=True), name="ui")
