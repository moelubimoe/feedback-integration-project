from fastapi import APIRouter
from app.schemas.feedback import FeedbackCreate
from app.services.producer import publish_to_queue

router = APIRouter()

@router.post("/feedback")
def create_feedback(feedback: FeedbackCreate):
    publish_to_queue(feedback.dict())
    return {
        "status": "queued",
        "message": "Заявка отправлена в очередь"
    }
from app.rabbit import publish_feedback  # импорт функции

@router.post("/feedback")
async def submit_feedback(feedback: FeedbackCreate):
    data = feedback.dict()
    publish_feedback(data)  # отправляем в RabbitMQ
    return {"status": "received", "data": data}
