from sqlalchemy import Column, Integer, BigInteger, Text, Boolean, Time
from backend.core.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(Text)
    fullname = Column(Text)
    task_creation_type = Column(Text, default="quick")
    notifications_enabled = Column(Boolean, default=False)
    notification_time = Column(Time)

    tags = relationship("Tag", back_populates="user", cascade="all, delete-orphan")
    spheres = relationship("Sphere", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete")
