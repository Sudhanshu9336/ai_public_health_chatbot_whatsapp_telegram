from fastapi import FastAPI, Request, BackgroundTasks, Body
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import httpx

from app.config import RASA_BASE_URL
from app.db import init_db, add_subscriber, remove_subscriber, list_subscribers, save_broadcast, get_broadcasts
from app.faqs import find_faq_answer, ask_gemini
from app.models import OutboundAlert, SubscriberIn
from app.messaging_utils import send_whatsapp_cloud, send_telegram

logger = logging.getLogger("uvicorn.error")
app = FastAPI(title="Public Health Chatbot Backend")

# Allow local frontend & webview to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}


# --- Hybrid handler: FAQ -> Gemini -> (optionally Rasa fallback) ---
async def _handle_message_and_reply(sender: str, message: str, channel: str):
    # Try FAQ first
    answer = find_faq_answer(message)
    if not answer:
        # Try Gemini fallback (if available)
        try:
            answer = await ask_gemini(message)
        except Exception as e:
            logger.warning("Gemini not available: %s", e)
            answer = None

    # Optionally forward to Rasa if still no answer
    if not answer:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.post(
                    f"{RASA_BASE_URL}/webhooks/rest/webhook",
                    json={"sender": sender, "message": message},
                )
                r.raise_for_status()
                data = r.json()
            answer = "\n".join([m.get("text", "") for m in data if m.get("text")])
        except Exception as e:
            logger.error("Rasa call failed: %s", e)
            answer = "Sorry, I couldn't get an answer right now. Please try again later."

    # Send back via channel
    if channel == "whatsapp":
        await send_whatsapp_cloud(sender, answer)
    elif channel == "telegram":
        await send_telegram(sender, answer)
    else:
        logger.info("Unknown channel, skipping send. channel=%s sender=%s", channel, sender)


# --- Webhook endpoints ---
@app.post("/webhook/whatsapp", response_class=PlainTextResponse)
async def webhook_whatsapp(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    try:
        entry = payload.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages") or []
        if not messages:
            return "OK"
        msg = messages[0]
        from_number = msg.get("from")
        text = (msg.get("text", {}) or {}).get("body") or msg.get("body") or ""
    except Exception:
        return "OK"

    background_tasks.add_task(_handle_message_and_reply, from_number, text, "whatsapp")
    return "200"


@app.post("/webhook/telegram", response_class=PlainTextResponse)
async def webhook_telegram(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    message = payload.get("message") or payload.get("edited_message") or {}
    text = message.get("text", "") or payload.get("callback_query", {}).get("data", "")
    chat = message.get("chat", {})
    chat_id = chat.get("id") or payload.get("callback_query", {}).get("from", {}).get("id")
    if not chat_id or not text:
        return "OK"

    background_tasks.add_task(_handle_message_and_reply, str(chat_id), text, "telegram")
    return "200"


# --- Subscribers ---
@app.post("/subscribers")
def add_subscriber_endpoint(s: SubscriberIn):
    add_subscriber(s.phone, s.language)
    return {"ok": True}


@app.get("/subscribers")
def get_subscribers_endpoint():
    subs = list_subscribers()
    return [{"phone": s.phone, "language": s.language} for s in subs]


@app.delete("/subscribers/{phone}")
def delete_subscriber(phone: str):
    remove_subscriber(phone)
    return {"ok": True}


# --- Broadcast ---
@app.post("/alerts/broadcast")
async def broadcast(alert: OutboundAlert):
    subs = list_subscribers()
    sent = 0
    for s in subs:
        body = alert.text
        if alert.channel in ["sms", "whatsapp"]:
            r = await send_whatsapp_cloud(s.phone, body)
        elif alert.channel in ["telegram", "tg"]:
            r = await send_telegram(s.phone, body)
        else:
            r = {"status": "skipped", "reason": "unknown channel"}

        if r.get("status") == "sent":
            sent += 1

    save_broadcast(alert.text, alert.channel)
    return {"sent": sent, "total": len(subs), "saved": True}


# --- History ---
@app.get("/history")
def history():
    return [
        {
            "id": b.id,
            "message": b.message,
            "channel": b.channel,
            "timestamp": b.timestamp.isoformat(),
        }
        for b in get_broadcasts()
    ]


# --- /ask for index.html webview ---
@app.post("/ask")
async def ask_endpoint(payload: dict = Body(...)):
    q = payload.get("question") or payload.get("message") or payload.get("text") or ""
    if not q:
        return {"answer": "⚠️ Please send a question in JSON as {\"question\": \"...\"}"}

    try:
        ans = find_faq_answer(q)
        if not ans:
            try:
                ans = await ask_gemini(q)
            except Exception:
                ans = None

        if not ans:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.post(
                    f"{RASA_BASE_URL}/webhooks/rest/webhook",
                    json={"sender": "webview", "message": q},
                )
                r.raise_for_status()
                data = r.json()
            ans = "\n".join([m.get("text", "") for m in data if m.get("text")]) or "Sorry, no answer."

        return {"answer": ans}
    except Exception as e:
        return {"answer": f"Error: {e}"}

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

# Hybrid handler: FAQ -> Gemini -> (optionally Rasa fallback)
async def _handle_message_and_reply(sender: str, message: str, channel: str):
    # Try FAQ first
    answer = find_faq_answer(message)
    if not answer:
        # Try Gemini fallback (if available)
        try:
            answer = await ask_gemini(message)
        except Exception as e:
            logger.warning("Gemini not available: %s", e)
            answer = None

    # Optionally forward to Rasa if still no answer
    if not answer:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.post(f"{RASA_BASE_URL}/webhooks/rest/webhook", json={"sender": sender, "message": message})
                r.raise_for_status()
                data = r.json()
            answer = "\n".join([m.get("text","") for m in data if m.get("text")])
        except Exception as e:
            logger.error("Rasa call failed: %s", e)
            answer = "Sorry, I couldn't get an answer right now. Please try again later."

    # Send back via channel
    if channel == "whatsapp":
        await send_whatsapp_cloud(sender, answer)
    elif channel == "telegram":
        await send_telegram(sender, answer)
    else:
        logger.info("Unknown channel, skipping send. channel=%s sender=%s", channel, sender)

# Webhook endpoints (WhatsApp/Telegram)
@app.post("/webhook/whatsapp", response_class=PlainTextResponse)
async def webhook_whatsapp(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    # minimal parsing for typical Meta WhatsApp Cloud payload
    try:
        entry = payload.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages") or []
        if not messages:
            return "OK"
        msg = messages[0]
        from_number = msg.get("from")
        text = (msg.get("text", {}) or {}).get("body") or msg.get("body") or ""
    except Exception:
        return "OK"

    background_tasks.add_task(_handle_message_and_reply, from_number, text, "whatsapp")
    return "200"

@app.post("/webhook/telegram", response_class=PlainTextResponse)
async def webhook_telegram(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    message = payload.get("message") or payload.get("edited_message") or {}
    text = message.get("text", "") or payload.get("callback_query", {}).get("data", "")
    chat = message.get("chat", {})
    chat_id = chat.get("id") or payload.get("callback_query", {}).get("from", {}).get("id")
    if not chat_id or not text:
        return "OK"
    background_tasks.add_task(_handle_message_and_reply, str(chat_id), text, "telegram")
    return "200"

# Subscribers
@app.post("/subscribers")
def add_subscriber_endpoint(s: SubscriberIn):
    add_subscriber(s.phone, s.language)
    return {"ok": True}

@app.get("/subscribers")
def get_subscribers_endpoint():
    subs = list_subscribers()
    return [{"phone": s.phone, "language": s.language} for s in subs]

@app.delete("/subscribers/{phone}")
def delete_subscriber(phone: str):
    remove_subscriber(phone)
    return {"ok": True}

# Broadcast
@app.post("/alerts/broadcast")
async def broadcast(alert: OutboundAlert):
    subs = list_subscribers()
    sent = 0
    for s in subs:
        # accept both "text" and older "message" naming; our OutboundAlert has "text"
        body = alert.text
        if alert.channel in ["sms", "whatsapp"]:
            r = await send_whatsapp_cloud(s.phone, body)
        elif alert.channel in ["telegram", "tg"]:
            r = await send_telegram(s.phone, body)
        else:
            r = {"status": "skipped", "reason": "unknown channel"}
        if r.get("status") == "sent":
            sent += 1
    save_broadcast(alert.text, alert.channel)
    return {"sent": sent, "total": len(subs), "saved": True}

# History
@app.get("/history")
def history():
    from .db import get_broadcasts
    return [
        {"id": b.id, "message": b.message, "channel": b.channel, "timestamp": b.timestamp.isoformat()}
        for b in get_broadcasts()
    ]

# /ask for index.html webview
@app.post("/ask")
async def ask_endpoint(payload: dict = Body(...)):
    q = payload.get("question") or payload.get("message") or payload.get("text") or ""
    if not q:
        return {"answer": "⚠️ Please send a question in JSON as {\"question\": \"...\"}"}
    # try FAQ/Gemini/Rasa via the same hybrid helper
    # For local tests, we can re-use _handle_message_and_reply but it sends outwards.
    try:
        # Try FAQ/Gemini/Rasa sequence but return answer directly (not sending over WhatsApp)
        ans = find_faq_answer(q)
        if not ans:
            try:
                ans = await ask_gemini(q)
            except Exception:
                ans = None
        if not ans:
            # call Rasa
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.post(f"{RASA_BASE_URL}/webhooks/rest/webhook", json={"sender": "webview", "message": q})
                r.raise_for_status()
                data = r.json()
            ans = "\n".join([m.get("text","") for m in data if m.get("text")]) or "Sorry, no answer."
        return {"answer": ans}
    except Exception as e:
        return {"answer": f"Error: {e}"}
