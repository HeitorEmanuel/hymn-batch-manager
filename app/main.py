from __future__ import annotations

import logging
import os
import platform
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMessageBox

from app.bootstrap import bootstrap
from app.config import AppConfig
from app.logging_config import configure_logging
from app.ui.main_window import MainWindow


def main() -> int:
    config = AppConfig.load()
    config.ensure_directories()
    configure_logging(config.log_dir)
    logger = logging.getLogger(__name__)
    logger.info(
        "Inicializando versão=%s sistema=%s dados=%s",
        config.version,
        platform.platform(),
        config.data_dir,
    )
    app = QApplication(sys.argv)
    app.setApplicationName(config.app_name)
    app.setApplicationVersion(config.version)
    try:
        container = bootstrap(config)
        window = MainWindow(container)
        window.show()
        if os.getenv("HBM_SMOKE_TEST") == "1":
            QTimer.singleShot(250, app.quit)
        return app.exec()
    except Exception as exc:
        logger.exception("Falha fatal na inicialização")
        QMessageBox.critical(
            None,
            "Falha ao iniciar",
            f"Não foi possível iniciar o Hymn Batch Manager.\n\nDetalhes: {exc}",
        )
        return 1
    finally:
        logger.info("Aplicação encerrada")


if __name__ == "__main__":
    raise SystemExit(main())
