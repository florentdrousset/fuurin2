from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from db.database import engine
from routers.api_v1 import router as v1_router

app = FastAPI(title="Fuurin API", version="0.3.0")

# CORS for local front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount versioned API
app.include_router(v1_router, prefix="/api/v1")


@app.get("/health", tags=["System"]) 
def health():
    return {"status": "ok"}


@app.get("/db/health", tags=["System"]) 
def db_health():
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {"status": "ok"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})


@app.get("/version", tags=["System"]) 
def version():
    return {"name": app.title, "version": app.version}


@app.get("/", tags=["System"]) 
def root():
    return JSONResponse({
        "message": "Fuurin API",
        "docs": "/docs",
        "health": "/health",
        "db_health": "/db/health",
        "v1": "/api/v1/health",
    })
