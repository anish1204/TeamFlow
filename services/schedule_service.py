from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.notification import Notification
from fastapi import HTTPException


# 🕒 Check user's meeting availability window
async def check_availability(db: Session, user_id: int, date_str: str, time_str: str):
    """
    Checks if the given user has a conflicting meeting within ±30 minutes
    of the target time.
    Returns a dict: { "available": bool, "conflict_time": str | None }
    """
    try:
        target_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        print("⚠️ Invalid date/time format:", date_str, time_str)
        return {"available": False, "conflict_time": None}

    start_window = target_dt - timedelta(minutes=30)
    end_window = target_dt + timedelta(minutes=30)

    print(f"🕒 Checking notifications for user {user_id} between {start_window} and {end_window}")

    existing = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .filter(Notification.date.isnot(None))
        .filter(Notification.time.isnot(None))
        .all()
    )

    for notif in existing:
        try:
            notif_dt = datetime.strptime(f"{notif.date} {notif.time}", "%Y-%m-%d %H:%M")
            if start_window <= notif_dt <= end_window:
                print(f"❌ Conflict with notification {notif.id} at {notif.time}")
                return {"available": False, "conflict_time": notif.time}
        except Exception as e:
            print(f"⚠️ Skipping invalid notification: {e}")

    print("✅ No conflicts found for this time slot.")
    return {"available": True, "conflict_time": None}

async def create_notification(
    db: Session,
    user_id: int,
    date: str,
    time: str,
    available: bool,
    conflict_time: str = None
):
    """
    Creates a new meeting notification only if no existing meeting is found
    for the same date and time.
    If one exists, returns an 'unavailable' response.
    """
    from main import sio  # lazy import to avoid circular dependency

    # 🕒 Check for existing meeting with same date & time
    existing = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.date == date,
            Notification.time == time,
        )
        .first()
    )

    if existing:
        print(f"❌ Duplicate meeting found for user {user_id} on {date} at {time}")
        return {
            "available": False,
            "conflict_time": existing.time,
            "message": "Slot already booked",
        }

    # ✅ Proceed to create new meeting suggestion
    notif = Notification(
        user_id=user_id,
        title="Meeting Suggestion",
        message=f"AI suggests meeting on {date} at {time}",
        date=date,
        time=time,
        available=available,
        status="UNAVAILABLE" if not available else "PENDING",
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)

    # 🔔 Emit socket event
    await sio.emit(
        "new_notification",
        {
            "title": notif.title,
            "date": notif.date,
            "time": notif.time,
            "available": notif.available,
            "conflictTime": conflict_time,
            "notification_id": notif.id,
        },
        to=f"user_{user_id}",
    )

    print(f"📢 Emitted new_notification to user_{user_id}")
    return {
        "available": True,
        "conflict_time": conflict_time,
        "notification": notif.id,
        "message": "Slot successfully created",
    }



# 📨 Respond to a meeting notification (Accept / Reject)
def respond_to_notification(db: Session, notif_id: int, response: str):
    """
    Updates the status of a notification based on user's response.
    """
    notif = db.query(Notification).filter(Notification.id == notif_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    response = response.lower().strip()
    if response not in ["yes", "no"]:
        raise HTTPException(status_code=400, detail="Response must be 'yes' or 'no'")

    notif.status = "ACCEPTED" if response == "yes" else "REJECTED"
    db.commit()
    db.refresh(notif)

    print(f"🟢 Notification {notif.id} marked as {notif.status}")
    return {"message": f"Notification {notif.id} marked as {notif.status}"}
