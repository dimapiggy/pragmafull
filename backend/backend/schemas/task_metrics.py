from pydantic import BaseModel, condecimal
from typing import Annotated

DecimalNum = Annotated[float, condecimal(ge=1, le=10, max_digits=5, decimal_places=2)]

class TaskMetricsBase(BaseModel):
    l: DecimalNum
    v: DecimalNum
    d: DecimalNum
    e: DecimalNum
    re: DecimalNum

class TaskMetricsCreate(TaskMetricsBase):
    task_id: int

class TaskMetricsUpdate(TaskMetricsBase):
    pass

class TaskMetricsRead(TaskMetricsBase):

    class Config:
        from_attributes = True
