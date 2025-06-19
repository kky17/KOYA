from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from .db import init_db, create_appointment, fetch_appointments

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="AI Integration Agency")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

init_db()

@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse(BASE_DIR / "static" / "index.html")

@app.post("/api/appointments")
async def create(name: str = Form(...), email: str = Form(...), datetime: str = Form(...), message: str = Form("")):
    create_appointment(name, email, datetime, message)
    return {"status": "created"}

@app.get("/api/appointments")
async def list_appointments():
    return fetch_appointments()
