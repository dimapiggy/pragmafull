from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.db import get_db
from backend.schemas.subtask import SubtaskCreate, SubtaskOut, SubtaskUpdate
from backend.crud.subtask import create_subtask, get_subtask, get_subtasks_by_task, update_subtask, delete_subtask
from backend.core.auth import get_current_user
from backend.models import User, Task

router = APIRouter(prefix="/subtasks", tags=["subtasks"])

# Создание подзадачи
@router.post("/", response_model=SubtaskOut)
def create(subtask: SubtaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Проверка, что задача принадлежит текущему пользователю
    task = db.query(Task).filter(Task.id == subtask.task_id).first()
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return create_subtask(db, subtask)

# Получение подзадачи по ID
@router.get("/{subtask_id}", response_model=SubtaskOut)
def read(subtask_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subtask = get_subtask(db, subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    
    task = db.query(Task).filter(Task.id == subtask.task_id).first()
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return subtask

@router.get("/task/{task_id}", response_model=list[SubtaskOut])
def read_by_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return get_subtasks_by_task(db, task_id)

@router.patch("/{subtask_id}", response_model=SubtaskOut)
def update(subtask_id: int, subtask_data: SubtaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subtask = get_subtask(db, subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    
    task = db.query(Task).filter(Task.id == subtask.task_id).first()
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return update_subtask(db, subtask_id, subtask_data)

@router.delete("/{subtask_id}", response_model=SubtaskOut)
def delete(subtask_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subtask = get_subtask(db, subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    
    task = db.query(Task).filter(Task.id == subtask.task_id).first()
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return delete_subtask(db, subtask_id)
