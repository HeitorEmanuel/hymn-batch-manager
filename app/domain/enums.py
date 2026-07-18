from __future__ import annotations

from enum import StrEnum


class RepertoireStatus(StrEnum):
    DRAFT = "rascunho"
    IN_PROGRESS = "em_andamento"
    COMPLETED = "concluido"
    CANCELLED = "cancelado"
    ERROR = "erro"


class ItemStatus(StrEnum):
    WAITING = "aguardando"
    SEARCHING = "pesquisando"
    RESULTS_FOUND = "resultados_encontrados"
    AWAITING_CONFIRMATION = "aguardando_confirmacao"
    CONFIRMED = "confirmado"
    QUEUED = "na_fila"
    DOWNLOADING = "baixando"
    COPYING = "copiando"
    CONVERTING = "convertendo"
    RENAMING = "renomeando"
    COMPLETED = "concluido"
    NOT_FOUND = "nao_encontrado"
    IGNORED = "ignorado"
    PAUSED = "pausado"
    CANCELLED = "cancelado"
    ERROR = "erro"


class MediaType(StrEnum):
    AUDIO = "audio"
    VIDEO = "video"
    KEEP_ORIGINAL = "manter_original"
