from sqlalchemy import Column, Integer, Numeric, ForeignKey
from backend.core.db import Base
from sqlalchemy.orm import relationship

class TaskMetrics(Base):
    __tablename__ = "task_metrics"

    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    l = Column(Numeric(5, 2), nullable=False)
    v = Column(Numeric(5, 2), nullable=False)
    d = Column(Numeric(5, 2), nullable=False)
    e = Column(Numeric(5, 2), nullable=False)
    re = Column(Numeric(5, 2), nullable=False)

    task = relationship("Task", back_populates="metrics")