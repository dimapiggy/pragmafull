from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from backend.schemas.subtask import SubtaskOut
from backend.schemas.tag import TagOut
from backend.schemas.sphere import SphereOut
from backend.schemas.task_metrics import TaskMetricsRead

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[float] = None
    is_done: Optional[bool] = False
    archived: Optional[bool] = False

class TaskCreate(TaskBase):
    tag_id: Optional[int] = None
    sphere_id: Optional[int] = None

class TaskUpdate(TaskBase):
    tag_id: Optional[int] = None
    sphere_id: Optional[int] = None

class TaskOut(TaskBase):
    id: int
    user_id: int
    subtasks: List[SubtaskOut] = []
    tag: Optional[TagOut] = None
    sphere: Optional[SphereOut] = None
    metrics: Optional[TaskMetricsRead]
    
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

