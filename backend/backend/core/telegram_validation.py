# backend/core/telegram_validation.py
import hashlib
import hmac
from urllib.parse import parse_qs, unquote
import json
from datetime import datetime, timedelta


def validate_telegram_initdata(init_data_str: str, bot_token: str, max_age_seconds: int = 86400):
    """
    Валидация initData от Telegram Web App
    
    Args:
        init_data_str: Строка initData из Telegram.WebApp.initData
        bot_token: Токен вашего бота от BotFather
        max_age_seconds: Максимальный возраст данных в секундах
    
    Returns:
        dict: Распарсенные данные если валидно, иначе None
    """
    if not init_data_str:
        return None
    
    try:
        # Парсим query строку
        parsed = parse_qs(init_data_str)
        
        # Получаем hash для проверки
        hash_value = parsed.get('hash')
        if not hash_value or not isinstance(hash_value, list):
            return None
        
        hash_str = hash_value[0]
        
        # Проверяем auth_date (давность данных)
        auth_date = parsed.get('auth_date')
        if not auth_date:
            return None
        
        auth_timestamp = int(auth_date[0])
        current_timestamp = int(datetime.now().timestamp())
        
        if current_timestamp - auth_timestamp > max_age_seconds:
            # Данные устарели
            return None
        
        # Подготавливаем строку для проверки
        data_check_string = prepare_data_check_string(parsed)
        
        # Создаем секретный ключ
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()
        
        # Вычисляем HMAC
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        # Сравниваем хэши
        if calculated_hash == hash_str:
            # Данные валидны, парсим user
            user_data = parse_user_data(parsed)
            return {
                'valid': True,
                'user': user_data,
                'auth_date': auth_timestamp,
                'query_id': parsed.get('query_id', [''])[0] if parsed.get('query_id') else None
            }
        else:
            return None
            
    except Exception as e:
        print(f"Validation error: {e}")
        return None


def prepare_data_check_string(parsed_data):
    """
    Подготавливает data_check_string для валидации
    Формат: key=value\nkey2=value2 (отсортировано по алфавиту, без поля hash)
    """
    # Фильтруем и сортируем
    filtered = {k: v[0] for k, v in parsed_data.items() if k != 'hash'}
    sorted_items = sorted(filtered.items())
    
    # Собираем строку
    return '\n'.join([f"{k}={v}" for k, v in sorted_items])


def parse_user_data(parsed_data):
    """Парсит данные пользователя из initData"""
    user_str = parsed_data.get('user')
    if not user_str:
        return None
    
    try:
        # user приходит как URL-encoded JSON строка
        if isinstance(user_str, list):
            user_str = user_str[0]
        
        user_json = unquote(user_str)
        user_data = json.loads(user_json)
        
        return {
            'id': user_data.get('id'),
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'username': user_data.get('username'),
            'language_code': user_data.get('language_code'),
            'is_premium': user_data.get('is_premium', False),
            'allows_write_to_pm': user_data.get('allows_write_to_pm', True),
            'photo_url': user_data.get('photo_url')
        }
    except Exception as e:
        print(f"Error parsing user data: {e}")
        return None