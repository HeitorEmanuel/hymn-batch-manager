from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.bootstrap import bootstrap
from app.config import AppConfig
from app.ui.main_window import MainWindow


def test_main_window_opens(qtbot: object, tmp_path: Path) -> None:
    config = AppConfig(
        app_name="Test",
        version="0",
        data_dir=tmp_path,
        database_url=f"sqlite:///{(tmp_path / 'database' / 'ui.db').as_posix()}",
        log_dir=tmp_path / "logs",
    )
    window = MainWindow(bootstrap(config))
    qtbot.addWidget(window)  # type: ignore[attr-defined]
    window.show()
    QApplication.processEvents()
    assert window.windowTitle() == "Test 0"
    assert window.home.table.rowCount() == 0
