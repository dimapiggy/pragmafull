from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from backend.models.task import Task
from backend.models.task_metrics import TaskMetrics
from backend.schemas.task import TaskCreate, TaskUpdate
from backend.crud.task_metrics import calculate_priority
from sqlalchemy.orm import joinedload
from backend.models.tag import Tag

def get_tasks(
    db: Session,
    user_id: int,
    archived: bool | None = None,
    overdue: bool | None = None,
    tag_id: int | None = None
):
    query = db.query(Task).filter(Task.user_id == user_id)

    if archived is not None:
        query = query.filter(Task.archived == archived)

    if overdue:
        query = query.filter(
            and_(
                Task.deadline < datetime.utcnow(),
                Task.archived == False
            )
        )

    if tag_id is not None:
        query = query.join(Task.tag, isouter=True).filter(Tag.id == tag_id)

    query = query.options(joinedload(Task.tag), joinedload(Task.subtasks))
    return query.all()


def get_task(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

def create_task(db: Session, task: TaskCreate, user_id: int):
    db_task = Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.flush()  

    metrics = TaskMetrics(
        task_id=db_task.id,
        l=0, v=0, d=0, e=0, re=0
    )
    db.add(metrics)

    # вычисляем приоритет задачи
    db_task.priority = calculate_priority(metrics)

    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: TaskUpdate, user_id: int):
    db_task = get_task(db, task_id, user_id)
    if not db_task:
        return None
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

# backend/crud/task.py
def delete_task(db: Session, task_id: int, user_id: int):
    db_task = get_task(db, task_id, user_id)
    if not db_task:
        return None
    
    # 1. Сначала удаляем связанные метрики
    if db_task.metrics:
        db.delete(db_task.metrics)
    
    # 2. Удаляем подзадачи (если cascade не работает)
    for subtask in db_task.subtasks:
        db.delete(subtask)
    
    # 3. Теперь удаляем саму задачу
    db.delete(db_task)
    db.commit()
    return db_task

def archive_task(db: Session, task_id: int, user_id: int, archive: bool = True):
    """Архивировать или разархивировать задачу"""
    db_task = get_task(db, task_id, user_id)
    if not db_task:
        return None
    
    db_task.archived = archive
    
    # ВАЖНО: Если архивируем задачу, она должна быть отмечена как выполненная
    # из-за CHECK constraint: (archived = false) OR (is_done = true)
    if archive:
        db_task.is_done = True
    # Если разархивируем, можно оставить is_done как есть
    # Или снять выполнение, если хотите:
    # if not archive:
    #     db_task.is_done = False
    
    db.commit()
    db.refresh(db_task)
    return db_task

def mark_task_done(db: Session, task_id: int, user_id: int):
    """Отметить задачу как выполненную (без обязательного архивирования)"""
    db_task = get_task(db, task_id, user_id)
    if not db_task:
        return None
    db_task.is_done = True
    # Убираем автоматическое архивирование, чтобы дать пользователю контроль
    # db_task.archived = True  # закомментируйте эту строку
    db.commit()
    db.refresh(db_task)
    return db_task

def mark_task_undone(db: Session, task_id: int, user_id: int):
    """Снять отметку о выполнении задачи"""
    db_task = get_task(db, task_id, user_id)
    if not db_task:
        return None
    db_task.is_done = False
    db.commit()
    db.refresh(db_task)
    return db_task