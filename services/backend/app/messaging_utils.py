import os
import httpx
import logging

logger = logging.getLogger(__name__)

# WhatsApp Cloud API (Meta) configuration
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_CLOUD_TOKEN = os.getenv("WHATSAPP_CLOUD_TOKEN", "")

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

async def send_whatsapp_cloud(to: str, body: str):
    """
    Sends a WhatsApp message via Meta's WhatsApp Cloud API.
    'to' should be a phone number in international format, e.g., '9198xxxxxxx' (no 'whatsapp:' prefix).
    """
    if not (WHATSAPP_PHONE_NUMBER_ID and WHATSAPP_CLOUD_TOKEN):
        return {"status": "skipped", "reason": "whatsapp cloud not configured"}
    url = f"https://graph.facebook.com/v16.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_CLOUD_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": body}
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            return {"status": "sent", "meta": r.json()}
    except Exception as e:
        logger.exception("WhatsApp Cloud send failed")
        return {"status": "error", "reason": str(e)}

async def send_telegram(chat_id: str, text: str):
    """
    Sends a Telegram message using the bot API.
    chat_id: the Telegram chat id (string or int)
    """
    if not TELEGRAM_BOT_TOKEN:
        return {"status": "skipped", "reason": "telegram not configured"}
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            return {"status": "sent", "meta": r.json()}
    except Exception as e:
        logger.exception("Telegram send failed")
        return {"status": "error", "reason": str(e)}
