from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from platformdirs import user_data_path


@dataclass(frozen=True, slots=True)
class AppConfig:
    app_name: str
    version: str
    data_dir: Path
    database_url: str
    log_dir: Path

    @classmethod
    def load(cls, *, development: bool | None = None) -> AppConfig:
        if development is None:
            development = os.getenv("HBM_DEVELOPMENT", "0") == "1"
        override = os.getenv("HBM_DATA_DIR")
        if override:
            data_dir = Path(override).expanduser().resolve()
        elif development:
            data_dir = (Path.cwd() / "data").resolve()
        else:
            data_dir = Path(user_data_path("HymnBatchManager", appauthor=False))
        database_path = data_dir / "database" / "hymn_batch_manager.db"
        return cls(
            app_name="Hymn Batch Manager",
            version="0.1.0",
            data_dir=data_dir,
            database_url=f"sqlite:///{database_path.as_posix()}",
            log_dir=data_dir / "logs",
        )

    def ensure_directories(self) -> None:
        for path in (
            self.data_dir,
            self.log_dir,
            self.data_dir / "database",
            self.data_dir / "temp",
        ):
            path.mkdir(parents=True, exist_ok=True)
