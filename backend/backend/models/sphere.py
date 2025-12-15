from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.db import Base
from backend.models.user import User  # для relationship

class Sphere(Base):
    __tablename__ = "spheres"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)

    user = relationship("User", back_populates="spheres")
    tasks = relationship("Task", back_populates="sphere")