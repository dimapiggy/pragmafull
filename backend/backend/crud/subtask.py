from sqlalchemy.orm import Session
from backend.models.subtask import Subtask
from backend.schemas.subtask import SubtaskCreate, SubtaskUpdate

def create_subtask(db: Session, subtask: SubtaskCreate):
    db_subtask = Subtask(**subtask.dict())
    db.add(db_subtask)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask

def get_subtask(db: Session, subtask_id: int):
    return db.query(Subtask).filter(Subtask.id == subtask_id).first()

def get_subtasks_by_task(db: Session, task_id: int):
    return db.query(Subtask).filter(Subtask.task_id == task_id).all()

def update_subtask(db: Session, subtask_id: int, subtask_data: SubtaskUpdate):
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if not subtask:
        return None
    for key, value in subtask_data.dict(exclude_unset=True).items():
        setattr(subtask, key, value)
    db.commit()
    db.refresh(subtask)
    return subtask

def delete_subtask(db: Session, subtask_id: int):
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if not subtask:
        return None
    db.delete(subtask)
    db.commit()
    return subtask
