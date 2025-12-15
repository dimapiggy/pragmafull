# alembic/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- make project package importable ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------------------------------------

config = context.config
fileConfig(config.config_file_name)

# ensure alembic uses DATABASE_URL if set, otherwise fallback to docker service db
db_url = os.getenv('DATABASE_URL', 'postgresql://dimaeboshi:1234@db:5432/postgres')
config.set_main_option('sqlalchemy.url', db_url)

# import your Base and make sure all models are imported so metadata is populated
# <-- adapt imports to your project: backend.models must expose Base or import models explicitly -->
from backend.core.db import Base  # <- обязательно, должен быть один Base.shared
# если backend.models не экспортирует все модели, явно импортируй их:
# from backend.models.user import User
# from backend.models.task import Task
# ...

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    context.configure(url=config.get_main_option("sqlalchemy.url"))
    with context.begin_transaction():
        context.run_migrations()
else:
    run_migrations_online()
