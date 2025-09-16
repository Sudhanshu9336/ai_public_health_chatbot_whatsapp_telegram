from pydantic import BaseModel

class RasaUserMsg(BaseModel):
    sender: str
    message: str
