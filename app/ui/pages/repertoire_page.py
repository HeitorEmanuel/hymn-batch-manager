from __future__ import annotations

from datetime import date
from pathlib import Path

from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.database.models import Repertoire
from app.domain.enums import MediaType
from app.services.repertoire_service import RepertoireInput
from app.utils.text import parse_name_list


class RepertoirePage(QWidget):
    save_requested = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self._names: list[str] = []
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 22, 28, 22)
        title = QLabel("Novo repertório")
        title.setStyleSheet("font-size: 26px; font-weight: 700;")
        root.addWidget(title)

        splitter = QSplitter()
        form_widget = QWidget()
        form = QFormLayout(form_widget)
        self.name = QLineEdit()
        self.name.setPlaceholderText("Ex.: Culto de domingo")
        self.description = QLineEdit()
        self.church = QLineEdit()
        self.event_input = QLineEdit()
        self.event_date = QDateEdit(QDate.currentDate())
        self.event_date.setCalendarPopup(True)
        destination_row = QWidget()
        destination_layout = QHBoxLayout(destination_row)
        destination_layout.setContentsMargins(0, 0, 0, 0)
        self.destination = QLineEdit(str(Path.home() / "Music" / "Hymn Batch Manager"))
        choose = QPushButton("Escolher…")
        choose.clicked.connect(self._choose_destination)
        destination_layout.addWidget(self.destination)
        destination_layout.addWidget(choose)
        self.media_type = QComboBox()
        self.media_type.addItem("Manter original", MediaType.KEEP_ORIGINAL)
        self.media_type.addItem("Áudio", MediaType.AUDIO)
        self.media_type.addItem("Vídeo", MediaType.VIDEO)
        self.output_format = QComboBox()
        self.output_format.addItems(["mp3", "manter original", "wav", "flac", "mp4"])
        self.quality = QComboBox()
        self.quality.addItems(["192 kbps", "128 kbps", "256 kbps", "320 kbps", "original"])
        self.numbering = QCheckBox("Numerar arquivos")
        self.numbering.setChecked(True)
        self.starting_number = QSpinBox()
        self.starting_number.setMinimum(1)
        self.starting_number.setMaximum(9999)
        self.generate_zip = QCheckBox("Gerar ZIP ao concluir")
        self.generate_zip.setChecked(True)
        form.addRow("Nome *", self.name)
        form.addRow("Descrição", self.description)
        form.addRow("Data", self.event_date)
        form.addRow("Igreja", self.church)
        form.addRow("Evento", self.event_input)
        form.addRow("Destino", destination_row)
        form.addRow("Tipo", self.media_type)
        form.addRow("Formato", self.output_format)
        form.addRow("Qualidade", self.quality)
        form.addRow("", self.numbering)
        form.addRow("Número inicial", self.starting_number)
        form.addRow("", self.generate_zip)

        names_widget = QWidget()
        names_layout = QVBoxLayout(names_widget)
        names_layout.setContentsMargins(12, 0, 0, 0)
        helper = QLabel("Cole nomes por linha, vírgula ou ponto e vírgula")
        helper.setStyleSheet("font-weight: 600;")
        self.raw_names = QTextEdit()
        self.raw_names.setPlaceholderText(
            "1. Grandioso És Tu\n02 - Porque Ele Vive\n• Alvo Mais Que a Neve"
        )
        controls = QHBoxLayout()
        clean_button = QPushButton("Limpar e organizar")
        clean_button.clicked.connect(self.clean_names)
        import_button = QPushButton("Importar TXT/CSV")
        import_button.clicked.connect(self._import_names)
        controls.addWidget(clean_button)
        controls.addWidget(import_button)
        controls.addStretch()
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["#", "Nome", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setDragDropMode(QTableWidget.DragDropMode.InternalMove)
        self.table.setDragDropOverwriteMode(False)
        names_layout.addWidget(helper)
        names_layout.addWidget(self.raw_names)
        names_layout.addLayout(controls)
        names_layout.addWidget(self.table)
        splitter.addWidget(form_widget)
        splitter.addWidget(names_widget)
        splitter.setSizes([410, 650])
        root.addWidget(splitter, 1)
        footer = QHBoxLayout()
        self.feedback = QLabel("Pronto para receber a lista.")
        save = QPushButton("Salvar repertório")
        save.setObjectName("primary")
        save.clicked.connect(self._save)
        footer.addWidget(self.feedback)
        footer.addStretch()
        footer.addWidget(save)
        root.addLayout(footer)

    def clean_names(self) -> None:
        result = parse_name_list(self.raw_names.toPlainText(), remove_duplicates=True)
        if result.duplicates:
            names = "\n".join(f"• {name}" for name in result.duplicates[:12])
            prompt = (
                f"Foram encontrados {len(result.duplicates)} duplicado(s):\n\n"
                f"{names}\n\nRemover os duplicados?"
            )
            answer = QMessageBox.question(
                self,
                "Itens duplicados encontrados",
                prompt,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            result = parse_name_list(
                self.raw_names.toPlainText(),
                remove_duplicates=answer == QMessageBox.StandardButton.Yes,
            )
        self._names = list(result.items)
        self._populate_table()
        self.feedback.setText(f"{len(self._names)} item(ns) preparado(s).")

    def _populate_table(self) -> None:
        self.table.setRowCount(len(self._names))
        for row, name in enumerate(self._names):
            position = QTableWidgetItem(str(row + 1))
            position.setFlags(position.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 0, position)
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem("Aguardando"))
        self.table.resizeColumnsToContents()

    def _table_names(self) -> tuple[str, ...]:
        names: list[str] = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            if item is not None and item.text().strip():
                names.append(item.text().strip())
        return tuple(names)

    def _save(self) -> None:
        if not self._names and self.raw_names.toPlainText().strip():
            self.clean_names()
        qdate = self.event_date.date()
        payload = RepertoireInput(
            name=self.name.text(),
            description=self.description.text(),
            event_date=date(qdate.year(), qdate.month(), qdate.day()),
            church=self.church.text(),
            event=self.event_input.text(),
            destination=Path(self.destination.text()),
            item_names=self._table_names(),
            default_format=self.output_format.currentText(),
            default_quality=self.quality.currentText(),
            default_media_type=self.media_type.currentData(),
            numbering_enabled=self.numbering.isChecked(),
            starting_number=self.starting_number.value(),
            generate_zip=self.generate_zip.isChecked(),
        )
        self.save_requested.emit(payload)

    def reset(self) -> None:
        self.name.clear()
        self.description.clear()
        self.church.clear()
        self.event_input.clear()
        self.raw_names.clear()
        self._names.clear()
        self.table.setRowCount(0)
        self.feedback.setText("Pronto para receber a lista.")

    def show_repertoire(self, repertoire: Repertoire) -> None:
        self.name.setText(repertoire.name)
        self.description.setText(repertoire.description or "")
        self.church.setText(repertoire.church or "")
        self.event_input.setText(repertoire.event or "")
        self.destination.setText(repertoire.destination_path)
        self._names = [item.original_name for item in repertoire.items]
        self.raw_names.setPlainText("\n".join(self._names))
        self._populate_table()
        self.feedback.setText(f"Repertório #{repertoire.id} aberto para consulta.")

    def _choose_destination(self) -> None:
        selected = QFileDialog.getExistingDirectory(self, "Escolher pasta de destino")
        if selected:
            self.destination.setText(selected)

    def _import_names(self) -> None:
        selected, _ = QFileDialog.getOpenFileName(
            self, "Importar lista", "", "Listas (*.txt *.csv);;Todos os arquivos (*)"
        )
        if not selected:
            return
        try:
            content = Path(selected).read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            QMessageBox.warning(self, "Não foi possível importar", str(exc))
            return
        self.raw_names.setPlainText(content)
        self.clean_names()
