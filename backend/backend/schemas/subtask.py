from pydantic import BaseModel

class SubtaskBase(BaseModel):
    task_id: int
    title: str
    is_done: bool = False

class SubtaskCreate(SubtaskBase):
    pass

class SubtaskUpdate(BaseModel):
    title: str | None = None
    is_done: bool | None = None

class SubtaskOut(SubtaskBase):
    id: int

    class Config:
        from_attributes = True

