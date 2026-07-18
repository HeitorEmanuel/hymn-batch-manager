from pathlib import Path

from sqlalchemy import inspect

from app.bootstrap import bootstrap
from app.config import AppConfig
from app.domain.enums import MediaType
from app.services.repertoire_service import RepertoireInput, RepertoireValidationError


def make_config(tmp_path: Path) -> AppConfig:
    return AppConfig(
        app_name="Test",
        version="0",
        data_dir=tmp_path,
        database_url=f"sqlite:///{(tmp_path / 'database' / 'test.db').as_posix()}",
        log_dir=tmp_path / "logs",
    )


def test_migration_creates_expected_tables(tmp_path: Path) -> None:
    container = bootstrap(make_config(tmp_path))
    database = tmp_path / "database" / "test.db"
    from app.database.session import create_database_engine

    tables = set(
        inspect(create_database_engine(f"sqlite:///{database.as_posix()}")).get_table_names()
    )
    assert {"repertoires", "repertoire_items", "library_files", "alembic_version"} <= tables
    assert container.repertoires.list_recent() == []


def test_create_and_reopen_repertoire(tmp_path: Path) -> None:
    container = bootstrap(make_config(tmp_path))
    created = container.repertoires.create(
        RepertoireInput(
            name="Culto",
            destination=tmp_path / "saida",
            item_names=("Grandioso És Tu", "Porque Ele Vive"),
            default_media_type=MediaType.AUDIO,
        )
    )
    reopened = container.repertoires.get(created.id)
    assert reopened is not None
    assert reopened.name == "Culto"
    assert [item.normalized_name for item in reopened.items] == [
        "grandioso es tu",
        "porque ele vive",
    ]


def test_create_rejects_empty_item_list(tmp_path: Path) -> None:
    container = bootstrap(make_config(tmp_path))
    try:
        container.repertoires.create(
            RepertoireInput(name="Vazio", destination=tmp_path, item_names=())
        )
    except RepertoireValidationError as exc:
        assert "pelo menos um" in str(exc)
    else:
        raise AssertionError("Era esperada validação")
