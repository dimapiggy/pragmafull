from fastapi import APIRouter, Response, HTTPException, Depends, Cookie, Header, Body, Request
from sqlalchemy.orm import Session
import jwt 
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from datetime import datetime
from urllib.parse import parse_qs, unquote
import json

from backend.core.db import get_db
from backend.models import User
from backend.core.config import auth_settings
from backend.core.config import settings
from backend.core.telegram_validation import validate_telegram_initdata

router = APIRouter(prefix="/auth")


def create_tokens(payload: dict):
    access_token = jwt.encode(
        {**payload, "exp": datetime.utcnow() + auth_settings.access_expire},
        auth_settings.jwt_access_secret,
        algorithm="HS256"
    )
    refresh_token = jwt.encode(
        {**payload, "exp": datetime.utcnow() + auth_settings.refresh_expire},
        auth_settings.jwt_refresh_secret,
        algorithm="HS256"
    )
    return access_token, refresh_token


def set_tokens_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="ACCESS_TOKEN",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="none",
        path="/"
    )
    response.set_cookie(
        key="REFRESH_TOKEN",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="none",
        path="/"
    )

def get_current_user(
    request: Request,
    response: Response,
    access_token: str | None = Cookie(default=None, alias="ACCESS_TOKEN"),
    refresh_token: str | None = Cookie(default=None, alias="REFRESH_TOKEN"),
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db)
) -> User:
    if not access_token and authorization and authorization.startswith("Bearer "):
        access_token = authorization[7:]

    if not access_token:
    # нет access токена → сразу пробуем refresh
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # пробуем обновить токен
        try:
            refresh_payload = jwt.decode(refresh_token, auth_settings.jwt_refresh_secret, algorithms=["HS256"])
            user = db.query(User).filter(
                User.id == refresh_payload.get("id"),
                User.telegram_id == refresh_payload.get("telegram_id")
            ).first()

            if not user:
                raise HTTPException(status_code=401, detail="User not found")

            new_payload = {"id": user.id, "telegram_id": user.telegram_id}
            new_access_token, new_refresh_token = create_tokens(new_payload)
            set_tokens_cookies(response, new_access_token, new_refresh_token)

            return user

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")


    try:
        payload = jwt.decode(access_token, auth_settings.jwt_access_secret, algorithms=["HS256"])
        user = db.query(User).filter(
            User.id == payload.get("id"),
            User.telegram_id == payload.get("telegram_id")
        ).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except ExpiredSignatureError:
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Token has expired. Please log in again.")


        try:
            refresh_payload = jwt.decode(refresh_token, auth_settings.jwt_refresh_secret, algorithms=["HS256"])
            user = db.query(User).filter(
                User.id == refresh_payload.get("id"),
                User.telegram_id == refresh_payload.get("telegram_id")
            ).first()

            if not user:
                raise HTTPException(status_code=401, detail="User not found")

            new_payload = {"id": user.id, "telegram_id": user.telegram_id}
            new_access_token, new_refresh_token = create_tokens(new_payload)
            set_tokens_cookies(response, new_access_token, new_refresh_token)
            return user

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired. Please log in again.")
        except PyJWTError:
            raise HTTPException(status_code=401, detail="Token has expired. Please log in again.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error during refresh: {str(e)}")

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token has expired. Please log in again.")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Возвращает данные текущего пользователя"""
    # 🔥 ВОЗВРАЩАЙ ПРОСТО user, А НЕ { "user": ... }
    return {
        "id": current_user.id,
        "telegram_id": current_user.telegram_id,
        "username": current_user.username,
        "fullname": current_user.fullname,
        "task_creation_type": current_user.task_creation_type,
        "notifications_enabled": current_user.notifications_enabled,
        "notification_time": str(current_user.notification_time) if current_user.notification_time else None
    }

# 1️⃣ Проверка пользователя по initData (без создания)
@router.post("/check")
def check_user(body: dict = Body(...), response: Response = None, db: Session = Depends(get_db)):
    init_data_str = body.get("initData")
    if not init_data_str:
        raise HTTPException(status_code=400, detail="No initData provided")

    parsed = parse_qs(init_data_str)
    user_str = parsed.get("user")
    if isinstance(user_str, list):
        user_str = user_str[0]

    try:
        user_data = json.loads(unquote(user_str))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user data in initData")

    tg_id = user_data.get("id")
    if not tg_id:
        raise HTTPException(status_code=400, detail="Telegram ID missing")

    user = db.query(User).filter(User.telegram_id == tg_id).first()

    # Если пользователь есть — выдаем токены и ВСЕ данные
    if user:
        payload = {"id": user.id, "telegram_id": user.telegram_id}
        access_token, refresh_token = create_tokens(payload)
        set_tokens_cookies(response, access_token, refresh_token)
        return {
            "exists": True,
            "prefill": {
                "id": user.id,
                "telegram_id": user.telegram_id,
                "username": user.username or "",
                "fullname": user.fullname or "",
                "task_creation_type": user.task_creation_type or "quick",
                "notifications_enabled": user.notifications_enabled or False,
                "notification_time": str(user.notification_time) if user.notification_time else "09:00:00"
            }
        }

    # Если нет — возвращаем данные из initData для автозаполнения формы
    fullname = (user_data.get("first_name", "") + " " + user_data.get("last_name", "")).strip()
    username = user_data.get("username")

    return {
        "exists": False,
        "prefill": {
            "fullname": fullname or "",
            "username": username or "",
            "task_creation_type": "quick",
            "notifications_enabled": False,
            "notification_time": "09:00:00"
        }
    }

# 2️⃣ Регистрация нового пользователя (создание в БД)
@router.post("/register")
def register_user(body: dict = Body(...), response: Response = None, db: Session = Depends(get_db)):
    init_data_str = body.get("initData")
    if not init_data_str:
        raise HTTPException(status_code=400, detail="No initData provided")

    parsed = parse_qs(init_data_str)
    user_str = parsed.get("user")
    if isinstance(user_str, list):
        user_str = user_str[0]

    try:
        user_data = json.loads(unquote(user_str))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user data in initData")

    tg_id = user_data.get("id")
    if not tg_id:
        raise HTTPException(status_code=400, detail="Telegram ID missing")

    # Проверяем, не зарегистрирован ли уже
    existing = db.query(User).filter(User.telegram_id == tg_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    # Берем данные от пользователя (он мог изменить fullname и т.д.)
    fullname = body.get("fullname")
    username = body.get("username", user_data.get("username"))
    task_creation_type = body.get("task_creation_type", "quick")
    notifications_enabled = body.get("notifications_enabled", False)
    notification_time = body.get("notification_time")

    # Создаем пользователя
    new_user = User(
        telegram_id=tg_id,
        username=username,
        fullname=fullname,
        task_creation_type=task_creation_type,
        notifications_enabled=notifications_enabled,
        notification_time=notification_time
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    payload = {"id": new_user.id, "telegram_id": new_user.telegram_id}
    access_token, refresh_token = create_tokens(payload)
    set_tokens_cookies(response, access_token, refresh_token)

    return {
        "success": True,
        "user": {
            "id": new_user.id,
            "telegram_id": new_user.telegram_id,
            "username": new_user.username,
            "fullname": new_user.fullname,
            "task_creation_type": new_user.task_creation_type,
            "notifications_enabled": new_user.notifications_enabled,
            "notification_time": str(new_user.notification_time) if new_user.notification_time else None
        }
    }

@router.post("/refresh")
def refresh_tokens(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias="REFRESH_TOKEN"),
    db: Session = Depends(get_db)
):
    """Отдельный эндпоинт для принудительного обновления токенов"""
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")
    
    try:
        payload = jwt.decode(refresh_token, auth_settings.jwt_refresh_secret, algorithms=["HS256"])
        user = db.query(User).filter(
            User.id == payload.get("id"),
            User.telegram_id == payload.get("telegram_id")
        ).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        new_payload = {"id": user.id, "telegram_id": user.telegram_id}
        new_access_token, new_refresh_token = create_tokens(new_payload)
        set_tokens_cookies(response, new_access_token, new_refresh_token)
        
        return {"success": True, "message": "Tokens refreshed"}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
@router.post("/debug/validate")
def debug_validate_initdata(body: dict = Body(...)):
    """Эндпоинт для отладки валидации initData"""
    init_data_str = body.get("initData")
    
    if not init_data_str:
        return {"error": "No initData provided"}
    
    # Пробуем распарсить без валидации
    parsed = parse_qs(init_data_str)
    
    result = {
        "raw_length": len(init_data_str),
        "parsed_keys": list(parsed.keys()),
        "has_hash": "hash" in parsed,
        "has_user": "user" in parsed,
        "has_auth_date": "auth_date" in parsed,
    }
    
    # Пробуем валидацию (если есть токен бота)
    if hasattr(settings, 'TELEGRAM_BOT_TOKEN') and settings.TELEGRAM_BOT_TOKEN:
        validation_result = validate_telegram_initdata(
            init_data_str=init_data_str,
            bot_token=settings.TELEGRAM_BOT_TOKEN
        )
        
        result["validation"] = {
            "is_valid": validation_result is not None,
            "user": validation_result.get('user') if validation_result else None,
            "auth_date": validation_result.get('auth_date') if validation_result else None
        }
    else:
        result["validation"] = {
            "is_valid": False,
            "error": "TELEGRAM_BOT_TOKEN not configured"
        }
    
    return result