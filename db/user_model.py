from sqlalchemy import Column, Integer, BigInteger, DateTime
from datetime import datetime
from user_bot.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    balance = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
