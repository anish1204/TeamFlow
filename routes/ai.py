# routes/ai.py

from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.message import Message
from typing import List, Optional
from models.user import User
from utils.auth import get_current_user
# from cohere import Client
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from datetime import datetime


router = APIRouter()

@router.post("/summarize/user/{other_user_id}")
def summarize_private_chat(
    other_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Step 1: Fetch chat messages between users
    messages = db.query(Message).filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.id.asc()).all()

    if not messages:
        return {"summary": "No messages found."}

    # Step 2: Format chat text
    chat_text = "\n".join([f"User {msg.sender_id}: {msg.content}" for msg in messages])

    # Step 3: Build prompt
    prompt_text = f"""
You are a smart assistant.

Given the following chat transcript, extract and summarize:
1. ✅ Tasks to be done
2. 📅 Meetings scheduled (with time if mentioned)
3. 💡 Key decisions or conclusions
4 . If any meeting then provide me the json in {"meetname":"","Date":"","Time":""}
Chat:
{chat_text}

Summarize now:
"""

    # Step 4: Call local LLaMA 3 via Ollama
    llm = Ollama(model="mistral")
    summary = llm.invoke(prompt_text)

    return {"summary": summary}


@router.post("/message/summarize")
def summarize_conv(payload: dict):
    # ==============================
    # 🚫 REAL AI CALL (DISABLED TEMPORARILY)
    #
    # from cohere import Client
    # co = Client("UbfqBunko7ITDMut3oB9m5Kc2wAF2xP0bWK5PX5Ztest")
    #
    # messages = payload.get("messages")
    # if not messages or not isinstance(messages, list):
    #     return {"error": "Payload must contain a 'messages' list."}
    #
    # chat_text = "\n".join(
    #     [f"User {m['sender_id']}: {m['content']}" for m in messages if m.get('content')]
    # )
    #
    # if len(chat_text.strip()) < 20:
    #     return {"summary": "Conversation is too short to summarize."}
    #
    # prompt_text = f\"\"\"You are a smart assistant.
    # Given the chat transcript below, summarize tasks, meetings, and decisions.
    # Chat:
    # {chat_text}
    # \"\"\"
    #
    # response = co.generate(model='command', prompt=prompt_text, max_tokens=300, temperature=0.3)
    # if response.generations and response.generations[0].text:
    #     return {"summary": response.generations[0].text.strip()}
    # else:
    #     return {"error": "No summary generated."}
    # ==============================

    # ✅ Mock local fallback summary
    mock_summary = {
        "summary": {
            "tasks": ["Update backend routes", "Add AI fallback response"],
            "meeting": {
                "meetname": "AI sync-up call",
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Time": "17:00"
            },
            "decisions": ["Temporarily disabled Cohere API to save credits"],
            "note": "⚠️ This is a simulated summary. Re-enable API when ready."
        }
    }
    return mock_summary



# @router.post("/message/summarize")
# def summarize_conv(payload: dict):
    from cohere import Client

    co = Client("UbfqBunko7ITDMut3oB9m5Kc2wAF2xP0bWK5PX5Ztest")

    # ✅ Validate and extract messages
    messages = payload.get("messages")
    if not messages or not isinstance(messages, list):
        return {"error": "Payload must contain a 'messages' list."}

    # ✅ Build chat text, skip empty content
    chat_text = "\n".join(
        [f"User {m['sender_id']}: {m['content']}" for m in messages if m.get("content")]
    )
    print(chat_text,'test')

    if len(chat_text.strip()) < 20:  # You can adjust this threshold
        return {
            "summary": "Conversation is too short to summarize. Try adding more messages."
        }

    # 📝 Custom prompt
    prompt_text = f"""
You are a smart assistant.

Given the following chat transcript, extract and summarize:
1. ✅ Tasks to be done
2. 📅 Meetings scheduled (with time if mentioned)
3. 💡 Key decisions or conclusions

Chat:
{chat_text}

Summarize now:
"""

    try:
        response = co.generate(
            model='command',  # or 'command-nightly' depending on your account
            prompt=prompt_text,
            max_tokens=300,
            temperature=0.3
        )

        # ✅ Defensive: check generations exist
        if response.generations and response.generations[0].text:
            return {"summary": response.generations[0].text.strip()}
        else:
            return {"error": "No summary generated."}

    except Exception as e:
        print(f"🔥 Error calling Cohere: {e}")
        return {"error": f"Failed to summarize conversation: {str(e)}"}
