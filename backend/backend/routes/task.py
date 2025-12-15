from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.core.db import get_db
from backend.schemas.task import TaskOut, TaskCreate, TaskUpdate
from backend.crud import task as crud_task
from backend.core.auth import get_current_user
from backend.models import User

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskOut])
def read_tasks(
    archived: Optional[bool] = None,
    overdue: Optional[bool] = None,
    tag_id: Optional[int] = Query(None, description="Фильтр по тегу"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получение задач пользователя с фильтрацией:
    - archived: показать архивные/неархивные задачи
    - overdue: показать просроченные задачи
    - tag_id: фильтр по тегу
    """
    return crud_task.get_tasks(
        db,
        user_id=current_user.id,
        archived=archived,
        overdue=overdue,
        tag_id=tag_id
    )

@router.get("/{task_id}", response_model=TaskOut)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = crud_task.get_task(db, task_id=task_id, user_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.post("/", response_model=TaskOut)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_task.create_task(db, task, user_id=current_user.id)

@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = crud_task.update_task(db, task_id, task, user_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}", response_model=TaskOut)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = crud_task.delete_task(db, task_id, user_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.patch("/{task_id}/done", response_model=TaskOut)
def mark_task_done(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Отметить задачу как выполненную"""
    db_task = crud_task.mark_task_done(db, task_id, user_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.patch("/{task_id}/undone", response_model=TaskOut)
def mark_task_undone(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Снять отметку о выполнении задачи"""
    db_task = crud_task.mark_task_undone(db, task_id, user_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.patch("/{task_id}/archive", response_model=TaskOut)
def archive_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Архивировать задачу"""
    db_task = crud_task.archive_task(db, task_id, user_id=current_user.id, archive=True)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.patch("/{task_id}/unarchive", response_model=TaskOut)
def unarchive_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Разархивировать задачу"""
    db_task = crud_task.archive_task(db, task_id, user_id=current_user.id, archive=False)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task