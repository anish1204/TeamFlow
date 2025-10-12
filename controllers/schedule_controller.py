from services.schedule_service import check_availability, create_notification, respond_to_notification

async def handle_suggestion(db, user_id, date, time):
    """
    Handles meeting suggestion logic — checks availability and creates a notification.
    """
    availability = await check_availability(db, user_id, date, time)

    available = availability.get("available", False)
    conflict_time = availability.get("conflict_time")

    notif = await create_notification(db, user_id, date, time, available, conflict_time)

    # 🧩 Handle both dict and model cases
    if isinstance(notif, dict):
        # Directly return backend’s dict (e.g. "Slot already booked")
        return {
            "available": notif.get("available", False),
            "conflict_time": notif.get("conflict_time"),
            "message": notif.get("message", "Unknown issue"),
        }

    # ✅ Normal flow — notification object created successfully
    return {
        "available": availability,
        "notification": {
            "id": notif.id,
            "title": notif.title,
            "status": notif.status,
            "date": notif.date,
            "time": notif.time,
        },
    }



def handle_response(db, notification_id, response):
    notif = respond_to_notification(db, notification_id, response)
    if not notif:
        return {"error": "Notification not found"}
    return {"message": f"Response saved: {notif.status}"}
