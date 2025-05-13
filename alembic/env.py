import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.models import task, user
from app.db.base_class import Base
from app.core.config import get_settings

# Alembic Config
config = context.config
fileConfig(config.config_file_name)

# Load DB URL from settings
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))

target_metadata = Base.metadata  # From your SQLAlchemy models

# Async migration run
def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    context.run_migrations()
else:
    asyncio.run(run_migrations_online())
