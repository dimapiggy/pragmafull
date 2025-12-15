from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.db import Base, engine
from backend.core.config import settings
from backend.routes import user, tag, sphere, task, subtask, task_metrics, test
from backend.core import auth

app = FastAPI(title=settings.PROJECT_NAME)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Nuxt dev
        "http://127.0.0.1:3000",      # Альтернативный адрес
        "http://localhost:8000",      # FastAPI сам себе
        "https://your-domain.com",    # Продакшен
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],  # ✅ Добавьте DELETE
    allow_headers=["*"],  # Или конкретные заголовки
    expose_headers=["*"],  # Важно для CORS с credentials
    max_age=600,  # Кешировать preflight запросы на 10 минут
)

app.include_router(user.router)
app.include_router(tag.router)
app.include_router(sphere.router)
app.include_router(task.router)
app.include_router(subtask.router)
app.include_router(task_metrics.router)
app.include_router(auth.router)
app.include_router(test.router)


@app.get("/ping")
def ping():
    return {"status": "ok"}
