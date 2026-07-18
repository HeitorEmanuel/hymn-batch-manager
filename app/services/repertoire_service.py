from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from app.database.models import Repertoire, RepertoireItem
from app.database.repositories import RepertoireRepository
from app.domain.enums import MediaType
from app.utils.text import normalize_name


@dataclass(frozen=True, slots=True)
class RepertoireInput:
    name: str
    destination: Path
    item_names: tuple[str, ...]
    description: str = ""
    event_date: date | None = None
    church: str = ""
    event: str = ""
    default_format: str = "mp3"
    default_quality: str = "192 kbps"
    default_media_type: MediaType = MediaType.KEEP_ORIGINAL
    numbering_enabled: bool = True
    starting_number: int = 1
    generate_zip: bool = True


class RepertoireValidationError(ValueError):
    pass


class RepertoireService:
    def __init__(self, repository: RepertoireRepository) -> None:
        self._repository = repository

    def create(self, data: RepertoireInput) -> Repertoire:
        name = data.name.strip()
        if not name:
            raise RepertoireValidationError("Informe um nome para o repertório.")
        if not data.item_names:
            raise RepertoireValidationError("Adicione pelo menos um hino ao repertório.")
        if data.starting_number < 1:
            raise RepertoireValidationError("O número inicial deve ser maior que zero.")
        destination = data.destination.expanduser()
        repertoire = Repertoire(
            name=name,
            description=data.description.strip() or None,
            event_date=data.event_date,
            church=data.church.strip() or None,
            event=data.event.strip() or None,
            destination_path=str(destination),
            default_format=data.default_format,
            default_quality=data.default_quality,
            default_media_type=data.default_media_type.value,
            numbering_enabled=data.numbering_enabled,
            starting_number=data.starting_number,
            generate_zip=data.generate_zip,
        )
        repertoire.items = [
            RepertoireItem(
                position=index,
                original_name=item_name,
                normalized_name=normalize_name(item_name),
                media_type=data.default_media_type.value,
                desired_format=data.default_format,
            )
            for index, item_name in enumerate(data.item_names, start=1)
        ]
        return self._repository.save(repertoire)

    def list_recent(self, *, limit: int = 20) -> list[Repertoire]:
        return self._repository.list_recent(limit=limit)

    def get(self, repertoire_id: int) -> Repertoire | None:
        return self._repository.get(repertoire_id)
