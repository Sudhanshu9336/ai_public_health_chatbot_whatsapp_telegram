from fastapi import FastAPI, Request, BackgroundTasks, Body, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import httpx
import os

from app.config import RASA_BASE_URL
from app.db import init_db, add_subscriber, remove_subscriber, list_subscribers, save_broadcast, get_broadcasts
from app.faqs import find_faq_answer, ask_gemini
from app.models import OutboundAlert, SubscriberIn
from app.messaging_utils import send_whatsapp_cloud, send_telegram

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Public Health Chatbot Backend",
    description="AI-driven multilingual health chatbot for disease awareness",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    """Initialize database and services on startup"""
    init_db()
    logger.info("🚀 Public Health Chatbot Backend started successfully")

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "public-health-chatbot-backend",
        "version": "1.0.0"
    }

# --- Core Message Processing ---
async def _handle_message_and_reply(sender: str, message: str, channel: str):
    """
    Hybrid message processing: FAQ → Gemini → Rasa fallback
    """
    try:
        # Step 1: Try FAQ first (fastest)
        answer = find_faq_answer(message)
        source = "FAQ"
        
        if not answer:
            # Step 2: Try Gemini AI (if available)
            try:
                answer = await ask_gemini(message)
                source = "Gemini"
            except Exception as e:
                logger.warning(f"Gemini not available: {e}")
                answer = None

        if not answer:
            # Step 3: Fallback to Rasa NLP
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        f"{RASA_BASE_URL}/webhooks/rest/webhook",
                        json={"sender": sender, "message": message},
                    )
                    response.raise_for_status()
                    data = response.json()
                
                answer = "\n".join([msg.get("text", "") for msg in data if msg.get("text")])
                source = "Rasa"
            except Exception as e:
                logger.error(f"Rasa call failed: {e}")
                answer = "Sorry, I couldn't process your request right now. Please try again later."
                source = "Error"

        # Add safety disclaimer for health-related responses
        if answer and any(keyword in message.lower() for keyword in ['symptom', 'disease', 'medicine', 'treatment']):
            answer += "\n\n⚠️ This is for information only. Please consult a healthcare professional for medical advice."

        # Send response via appropriate channel
        if channel == "whatsapp":
            result = await send_whatsapp_cloud(sender, answer)
        elif channel == "telegram":
            result = await send_telegram(sender, answer)
        else:
            logger.warning(f"Unknown channel: {channel}")
            return

        logger.info(f"Message processed - Channel: {channel}, Source: {source}, Status: {result.get('status', 'unknown')}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        # Send error message to user
        error_msg = "Sorry, there was a technical issue. Please try again."
        if channel == "whatsapp":
            await send_whatsapp_cloud(sender, error_msg)
        elif channel == "telegram":
            await send_telegram(sender, error_msg)

# --- Webhook Endpoints ---
@app.post("/webhook/whatsapp", response_class=PlainTextResponse)
async def webhook_whatsapp(request: Request, background_tasks: BackgroundTasks):
    """WhatsApp Cloud API webhook handler"""
    try:
        payload = await request.json()
        
        # Parse WhatsApp webhook payload
        entry = payload.get("entry", [])
        if not entry:
            return "OK"
            
        changes = entry[0].get("changes", [])
        if not changes:
            return "OK"
            
        value = changes[0].get("value", {})
        messages = value.get("messages", [])
        
        if not messages:
            return "OK"
            
        message = messages[0]
        from_number = message.get("from")
        text_body = message.get("text", {}).get("body", "") if message.get("text") else ""
        
        if from_number and text_body:
            background_tasks.add_task(_handle_message_and_reply, from_number, text_body, "whatsapp")
            
    except Exception as e:
        logger.error(f"WhatsApp webhook error: {e}")
    
    return "OK"

@app.post("/webhook/telegram", response_class=PlainTextResponse)
async def webhook_telegram(request: Request, background_tasks: BackgroundTasks):
    """Telegram Bot API webhook handler"""
    try:
        payload = await request.json()
        
        # Parse Telegram webhook payload
        message = payload.get("message", {})
        if not message:
            return "OK"
            
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        text = message.get("text", "")
        
        if chat_id and text:
            background_tasks.add_task(_handle_message_and_reply, str(chat_id), text, "telegram")
            
    except Exception as e:
        logger.error(f"Telegram webhook error: {e}")
    
    return "OK"

# --- Subscriber Management ---
@app.post("/subscribers")
async def add_subscriber_endpoint(subscriber: SubscriberIn):
    """Add new subscriber for alerts"""
    try:
        add_subscriber(subscriber.phone, subscriber.language)
        return {"success": True, "message": "Subscriber added successfully"}
    except Exception as e:
        logger.error(f"Error adding subscriber: {e}")
        raise HTTPException(status_code=500, detail="Failed to add subscriber")

@app.get("/subscribers")
async def get_subscribers_endpoint():
    """Get all subscribers"""
    try:
        subscribers = list_subscribers()
        return [{"phone": s.phone, "language": s.language} for s in subscribers]
    except Exception as e:
        logger.error(f"Error fetching subscribers: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch subscribers")

@app.delete("/subscribers/{phone}")
async def delete_subscriber_endpoint(phone: str):
    """Remove subscriber"""
    try:
        remove_subscriber(phone)
        return {"success": True, "message": "Subscriber removed successfully"}
    except Exception as e:
        logger.error(f"Error removing subscriber: {e}")
        raise HTTPException(status_code=500, detail="Failed to remove subscriber")

# --- Broadcast System ---
@app.post("/alerts/broadcast")
async def broadcast_alert(alert: OutboundAlert):
    """Broadcast alert to all subscribers"""
    try:
        subscribers = list_subscribers()
        sent_count = 0
        failed_count = 0
        
        for subscriber in subscribers:
            try:
                if alert.channel in ["whatsapp", "sms"]:
                    result = await send_whatsapp_cloud(subscriber.phone, alert.text)
                elif alert.channel in ["telegram", "tg"]:
                    result = await send_telegram(subscriber.phone, alert.text)
                else:
                    logger.warning(f"Unknown channel: {alert.channel}")
                    continue
                
                if result.get("status") == "sent":
                    sent_count += 1
                else:
                    failed_count += 1
                    
            except Exception as e:
                logger.error(f"Failed to send to {subscriber.phone}: {e}")
                failed_count += 1
        
        # Save broadcast to history
        save_broadcast(alert.text, alert.channel)
        
        return {
            "success": True,
            "sent": sent_count,
            "failed": failed_count,
            "total": len(subscribers)
        }
        
    except Exception as e:
        logger.error(f"Broadcast error: {e}")
        raise HTTPException(status_code=500, detail="Failed to send broadcast")

# --- History & Analytics ---
@app.get("/history")
async def get_broadcast_history():
    """Get broadcast history"""
    try:
        broadcasts = get_broadcasts()
        return [
            {
                "id": b.id,
                "message": b.message,
                "channel": b.channel,
                "timestamp": b.timestamp.isoformat(),
            }
            for b in broadcasts
        ]
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch history")

# --- Direct Chat API ---
@app.post("/ask")
async def ask_endpoint(payload: dict = Body(...)):
    """Direct chat API for testing and web interface"""
    try:
        question = payload.get("question") or payload.get("message") or payload.get("text", "")
        
        if not question.strip():
            return {"answer": "⚠️ Please provide a question"}
        
        # Use same processing logic as webhooks
        answer = find_faq_answer(question)
        source = "FAQ"
        
        if not answer:
            try:
                answer = await ask_gemini(question)
                source = "Gemini"
            except Exception:
                answer = None
        
        if not answer:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        f"{RASA_BASE_URL}/webhooks/rest/webhook",
                        json={"sender": "web_user", "message": question},
                    )
                    response.raise_for_status()
                    data = response.json()
                
                answer = "\n".join([msg.get("text", "") for msg in data if msg.get("text")])
                source = "Rasa"
            except Exception as e:
                logger.error(f"Rasa error in /ask: {e}")
                answer = "Sorry, I couldn't process your question right now."
                source = "Error"
        
        # Add disclaimer for health queries
        if answer and any(keyword in question.lower() for keyword in ['symptom', 'disease', 'medicine', 'treatment']):
            answer += "\n\n⚠️ This is for information only. Please consult a healthcare professional for medical advice."
        
        return {
            "answer": answer,
            "source": source,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error in /ask endpoint: {e}")
        return {
            "answer": "Sorry, there was an error processing your question.",
            "source": "Error",
            "success": False
        }

# --- Analytics Endpoints ---
@app.get("/analytics/stats")
async def get_analytics_stats():
    """Get basic analytics statistics"""
    try:
        subscribers = list_subscribers()
        broadcasts = get_broadcasts()
        
        # Language distribution
        lang_dist = {}
        for sub in subscribers:
            lang = sub.language
            lang_dist[lang] = lang_dist.get(lang, 0) + 1
        
        return {
            "total_subscribers": len(subscribers),
            "total_broadcasts": len(broadcasts),
            "language_distribution": lang_dist,
            "recent_broadcasts": len([b for b in broadcasts[-10:]]),  # Last 10
        }
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch analytics")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)