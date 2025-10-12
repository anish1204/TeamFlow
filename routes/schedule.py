from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.orm import Session
from db import get_db
from controllers.schedule_controller import handle_suggestion, handle_response

router = APIRouter(prefix="/schedule", tags=["Schedule"])

@router.post("/suggest")
async def suggest_meeting(data: dict, db: Session = Depends(get_db)):
    """
    Suggest a meeting time for a given user.
    Expected payload: { "user_id": int, "date": "YYYY-MM-DD", "time": "HH:MM" }
    """
    try:
        user_id = data.get("user_id")
        date = data.get("date")
        time = data.get("time")

        if not all([user_id, date, time]):
            raise HTTPException(status_code=400, detail="user_id, date, and time are required")

        result = await handle_suggestion(db, user_id, date, time)
        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/respond")
def respond_notification(data: dict, db: Session = Depends(get_db)):
    """
    Example input: { "notification_id": 5, "response": "yes" }
    """
    notif_id = data.get("notification_id")
    response = data.get("response")
    return handle_response(db, notif_id, response)

@router.get("/notifications/{user_id}")
def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    from models.notification import Notification
    return db.query(Notification).filter(Notification.user_id == user_id).all()

