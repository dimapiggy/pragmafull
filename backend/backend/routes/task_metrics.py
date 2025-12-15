from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.core.db import get_db
from backend import crud
from backend.schemas.task_metrics import TaskMetricsRead, TaskMetricsUpdate
from backend.core.auth import get_current_user
from backend.models import User

router = APIRouter(prefix="/task-metrics", tags=["task_metrics"])

# Получение метрик задачи (только своей)
@router.get("/{task_id}", response_model=TaskMetricsRead)
def read_task_metrics(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    metrics = crud.task_metrics.get_task_metrics(db, task_id)
    task = db.query(crud.task_metrics.Task).filter(crud.task_metrics.Task.id == task_id).first()

    if not metrics or not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Metrics not found")

    return metrics

# Обновление метрик задачи (только своей)
@router.put("/{task_id}")
def update_metrics(
    task_id: int,
    metrics_update: TaskMetricsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(crud.task_metrics.Task).filter(crud.task_metrics.Task.id == task_id).first()

    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    result = crud.task_metrics.update_task_metrics(db, task_id, metrics_update)
    if not result:
        raise HTTPException(status_code=404, detail="Metrics not found")

    db_metrics, task = result

    return JSONResponse(content={
        "metrics": {
            "l": float(db_metrics.l) if db_metrics.l is not None else None,
            "v": float(db_metrics.v) if db_metrics.v is not None else None,
            "d": float(db_metrics.d) if db_metrics.d is not None else None,
            "e": float(db_metrics.e) if db_metrics.e is not None else None,
            "re": float(db_metrics.re) if db_metrics.re is not None else None,
        },
        "task_priority": float(task.priority) if task and task.priority is not None else None
    })
