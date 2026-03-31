from sqlalchemy import Column, Integer, String, Boolean
from user_bot.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    reward = Column(Integer)
    is_active = Column(Boolean, default=True)
