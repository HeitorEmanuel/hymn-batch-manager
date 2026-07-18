from __future__ import annotations

import logging

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.bootstrap import Container
from app.services.repertoire_service import RepertoireInput, RepertoireValidationError
from app.ui.pages.home_page import HomePage
from app.ui.pages.repertoire_page import RepertoirePage
from app.ui.styles import DARK, LIGHT

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, container: Container) -> None:
        super().__init__()
        self.container = container
        self._dark = False
        self.setWindowTitle(f"{container.config.app_name} {container.config.version}")
        self.setMinimumSize(1000, 680)
        self.resize(1240, 780)
        central = QWidget()
        shell = QHBoxLayout(central)
        shell.setContentsMargins(0, 0, 0, 0)
        shell.setSpacing(0)
        shell.addWidget(self._build_sidebar())
        self.stack = QStackedWidget()
        self.home = HomePage()
        self.repertoire = RepertoirePage()
        self.stack.addWidget(self.home)
        self.stack.addWidget(self.repertoire)
        shell.addWidget(self.stack, 1)
        self.setCentralWidget(central)
        self.setStyleSheet(LIGHT)
        self.statusBar().showMessage("Dados locais • sem telemetria • FFmpeg não verificado")
        self.home.new_requested.connect(self.show_new_repertoire)
        self.home.open_requested.connect(self.open_repertoire)
        self.repertoire.save_requested.connect(self.save_repertoire)
        self._create_shortcuts()
        self.refresh_home()

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 24, 16, 18)
        logo = QLabel("♫  HYMN\n    BATCH MANAGER")
        logo.setStyleSheet("font-size: 16px; font-weight: 700;")
        layout.addWidget(logo)
        layout.addSpacing(24)
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        entries = [
            ("Início", 0, True),
            ("Repertórios", 1, True),
            ("Biblioteca", -1, False),
            ("Pesquisar", -1, False),
            ("Downloads", -1, False),
            ("Histórico", -1, False),
            ("Configurações", -1, False),
        ]
        for label, page, enabled in entries:
            button = QPushButton(label)
            button.setObjectName("navButton")
            button.setCheckable(enabled)
            button.setEnabled(enabled)
            if enabled:
                self.nav_group.addButton(button)
                button.clicked.connect(lambda _checked=False, index=page: self._navigate(index))
            else:
                button.setToolTip("Disponível em uma próxima etapa do MVP")
            layout.addWidget(button)
            if label == "Início":
                button.setChecked(True)
        layout.addStretch()
        theme = QPushButton("Alternar tema")
        theme.clicked.connect(self.toggle_theme)
        layout.addWidget(theme)
        notice = QLabel(
            "Arquivos locais e downloads autorizados. Você é responsável pelas permissões de uso."
        )
        notice.setWordWrap(True)
        notice.setStyleSheet("font-size: 11px; color: #9aabc5;")
        layout.addWidget(notice)
        return sidebar

    def _create_shortcuts(self) -> None:
        new_action = QAction(self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.show_new_repertoire)
        self.addAction(new_action)
        save_action = QAction(self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.repertoire._save)
        self.addAction(save_action)

    def _navigate(self, index: int) -> None:
        if index == 0:
            self.refresh_home()
        elif index == 1:
            self.show_new_repertoire()

    def show_new_repertoire(self) -> None:
        self.repertoire.reset()
        self.stack.setCurrentWidget(self.repertoire)

    def refresh_home(self) -> None:
        self.home.set_repertoires(self.container.repertoires.list_recent())
        self.stack.setCurrentWidget(self.home)

    def save_repertoire(self, payload: RepertoireInput) -> None:
        try:
            saved = self.container.repertoires.create(payload)
        except RepertoireValidationError as exc:
            QMessageBox.warning(self, "Revise o repertório", str(exc))
            return
        except Exception:
            logger.exception("Erro ao salvar repertório")
            QMessageBox.critical(
                self,
                "Não foi possível salvar",
                "O repertório não foi salvo. Consulte os logs para detalhes técnicos.",
            )
            return
        QMessageBox.information(
            self,
            "Repertório salvo",
            f"“{saved.name}” foi salvo com {len(saved.items)} item(ns).",
        )
        self.refresh_home()

    def open_repertoire(self, repertoire_id: int) -> None:
        repertoire = self.container.repertoires.get(repertoire_id)
        if repertoire is None:
            QMessageBox.warning(
                self, "Repertório não encontrado", "Atualize a lista e tente novamente."
            )
            return
        self.repertoire.show_repertoire(repertoire)
        self.stack.setCurrentWidget(self.repertoire)

    def toggle_theme(self) -> None:
        self._dark = not self._dark
        self.setStyleSheet(DARK if self._dark else LIGHT)
