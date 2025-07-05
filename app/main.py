from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.services.producer import publish_to_queue
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.models import Feedback, Base  # модель перенесена в models.py
import os

app = FastAPI()

# Шаблоны и статика
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Подключение к PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "feedback_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "feedback_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# 👇 Главная страница
@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 👇 Получение данных из формы
class FeedbackSchema(BaseModel):
    name: str
    email: str
    message: str
    source: str

@app.post("/feedback")
async def receive_feedback(data: FeedbackSchema):
    publish_to_queue(data.model_dump())
    return {"message": "Заявка отправлена!"}

# 👇 Отображение заявок из PostgreSQL
@app.get("/submissions", response_class=HTMLResponse)
def show_submissions(request: Request):
    session = SessionLocal()
    submissions = session.query(Feedback).order_by(Feedback.created_at.desc()).all()
    session.close()
    return templates.TemplateResponse("submissions.html", {
        "request": request,
        "submissions": submissions
    })

