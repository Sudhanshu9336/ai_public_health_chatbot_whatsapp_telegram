from pydantic import BaseModel

class OutboundAlert(BaseModel):
    text: str
    channel: str = "whatsapp"

class SubscriberIn(BaseModel):
    phone: str
    language: str = "en"

class InboundMessage(BaseModel):
    sender: str
    message: str
    channel: str
