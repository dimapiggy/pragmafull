from sqlalchemy import Column, Integer, Text, Boolean, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from backend.core.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="SET NULL"), nullable=True)
    sphere_id = Column(Integer, ForeignKey("spheres.id", ondelete="SET NULL"), nullable=True)

    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    priority = Column(Numeric(3,1), nullable=True)
    is_done = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="tasks")
    tag = relationship("Tag", back_populates="tasks",  lazy="joined")
    sphere = relationship("Sphere", back_populates="tasks",  lazy="joined")
    subtasks = relationship("Subtask", back_populates="task", cascade="all, delete", lazy="joined")
    metrics = relationship("TaskMetrics", back_populates="task", uselist=False)
    
