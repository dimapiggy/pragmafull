from sqlalchemy.orm import Session
from backend.models.task_metrics import TaskMetrics
from backend.models.task import Task
from backend.schemas.task_metrics import TaskMetricsCreate, TaskMetricsUpdate

def calculate_priority(metrics: TaskMetrics) -> float:
    numerator = 1.2 * metrics.l + metrics.v + metrics.d
    denominator = metrics.e + metrics.re
    if denominator == 0:
        return 0
    return numerator / denominator


def create_task_metrics(db: Session, metrics: TaskMetricsCreate):
    db_metrics = TaskMetrics(**metrics.dict())
    db.add(db_metrics)
    db.commit()
    db.refresh(db_metrics)
    return db_metrics


def get_task_metrics(db: Session, task_id: int):
    return db.query(TaskMetrics).filter(TaskMetrics.task_id == task_id).first()


def update_task_metrics(db: Session, task_id: int, metrics: TaskMetricsUpdate):
    db_metrics = get_task_metrics(db, task_id)
    if not db_metrics:
        return None

    for field, value in metrics.dict(exclude_unset=True).items():
        setattr(db_metrics, field, value)

    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.priority = calculate_priority(db_metrics)

    db.flush()
    db.commit()

    db.refresh(db_metrics)
    if task:
        db.refresh(task)

    return db_metrics, task
