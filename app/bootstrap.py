from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from alembic import command
from alembic.config import Config

from app.config import AppConfig
from app.database.repositories import RepertoireRepository
from app.database.session import SessionFactory, create_database_engine
from app.services.repertoire_service import RepertoireService


@dataclass(frozen=True, slots=True)
class Container:
    config: AppConfig
    repertoires: RepertoireService


def run_migrations(config: AppConfig) -> None:
    project_root = Path(__file__).resolve().parent.parent
    alembic = Config(str(project_root / "alembic.ini"))
    alembic.attributes["configure_logger"] = False
    alembic.set_main_option("script_location", str(project_root / "migrations"))
    alembic.set_main_option("sqlalchemy.url", config.database_url.replace("%", "%%"))
    command.upgrade(alembic, "head")


def bootstrap(config: AppConfig | None = None) -> Container:
    active_config = config or AppConfig.load()
    active_config.ensure_directories()
    run_migrations(active_config)
    engine = create_database_engine(active_config.database_url)
    sessions = SessionFactory(engine)
    repository = RepertoireRepository(sessions)
    return Container(active_config, RepertoireService(repository))
