from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.database.models import Repertoire


class HomePage(QWidget):
    new_requested = Signal()
    open_requested = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)
        heading = QLabel("Início")
        heading.setStyleSheet("font-size: 26px; font-weight: 700;")
        subtitle = QLabel("Organize seus repertórios e mídias locais em um só lugar.")
        subtitle.setStyleSheet("color: #7c8799;")
        layout.addWidget(heading)
        layout.addWidget(subtitle)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 18)
        self.total_label = QLabel("0 repertórios salvos")
        self.total_label.setStyleSheet("font-size: 18px; font-weight: 600;")
        new_button = QPushButton("Novo repertório")
        new_button.setObjectName("primary")
        new_button.clicked.connect(self.new_requested)
        card_layout.addWidget(self.total_label)
        card_layout.addStretch()
        card_layout.addWidget(new_button)
        layout.addWidget(card)

        recent_label = QLabel("Repertórios recentes")
        recent_label.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(recent_label)
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Nome", "Data", "Itens", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self._open_row)
        layout.addWidget(self.table, 1)

    def set_repertoires(self, repertoires: list[Repertoire]) -> None:
        self.total_label.setText(f"{len(repertoires)} repertório(s) salvo(s)")
        self.table.setRowCount(len(repertoires))
        for row, repertoire in enumerate(repertoires):
            name = QTableWidgetItem(repertoire.name)
            name.setData(256, repertoire.id)
            self.table.setItem(row, 0, name)
            self.table.setItem(row, 1, QTableWidgetItem(repertoire.created_at.strftime("%d/%m/%Y")))
            self.table.setItem(row, 2, QTableWidgetItem(str(len(repertoire.items))))
            self.table.setItem(
                row, 3, QTableWidgetItem(repertoire.status.replace("_", " ").title())
            )

    def _open_row(self, row: int, _column: int) -> None:
        item = self.table.item(row, 0)
        if item is not None:
            self.open_requested.emit(int(item.data(256)))
