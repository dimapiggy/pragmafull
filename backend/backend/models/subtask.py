from sqlalchemy import Column, Integer, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.db import Base
from backend.models.task import Task

class Subtask(Base):
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=False)
    is_done = Column(Boolean, default=False)

    task = relationship("Task", back_populates="subtasks")
