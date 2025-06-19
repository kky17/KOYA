from fastapi import FastAPI
from pydantic import BaseModel
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
    """Serve the landing page.

    Using ``HTMLResponse`` ensures browsers display the page instead of
    triggering a download when ``HEAD`` requests are made.
    """
    index_path = BASE_DIR / "static" / "index.html"
    return HTMLResponse(index_path.read_text())

class AppointmentIn(BaseModel):
    name: str
    email: str
    datetime: str
    message: str | None = None


@app.post("/api/appointments")
async def create(app_data: AppointmentIn):
    create_appointment(
        app_data.name,
        app_data.email,
        app_data.datetime,
        app_data.message or "",
    )
    return {"status": "created"}

@app.get("/api/appointments")
async def list_appointments():
    return fetch_appointments()
