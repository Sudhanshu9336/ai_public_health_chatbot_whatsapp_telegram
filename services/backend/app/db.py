import os
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List
from datetime import datetime
from .config import SQLITE_DB

# Ensure absolute path and folder exists
db_path = os.path.abspath(SQLITE_DB)
os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)

engine = create_engine(f"sqlite:///{db_path}", echo=False)

class Subscriber(SQLModel, table=True):
    phone: str = Field(primary_key=True)
    language: str = Field(default="en")

class Broadcast(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    message: str
    channel: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

def init_db():
    SQLModel.metadata.create_all(engine)

def add_subscriber(phone: str, language: str = "en"):
    with Session(engine) as session:
        s = Subscriber(phone=phone, language=language or "en")
        session.merge(s)
        session.commit()

def remove_subscriber(phone: str):
    with Session(engine) as session:
        s = session.get(Subscriber, phone)
        if s:
            session.delete(s)
            session.commit()

def list_subscribers() -> List[Subscriber]:
    with Session(engine) as session:
        return list(session.exec(select(Subscriber)))

def save_broadcast(message: str, channel: str):
    with Session(engine) as session:
        b = Broadcast(message=message, channel=channel)
        session.add(b)
        session.commit()

def get_broadcasts():
    with Session(engine) as session:
        return list(session.exec(select(Broadcast).order_by(Broadcast.timestamp.desc())))
