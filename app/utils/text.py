from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

_PREFIX_RE = re.compile(
    r"^\s*(?:(?:\d{1,4})\s*[.)\-\u2013\u2014:]\s*|[•·▪◦*]+\s*|[-\u2013\u2014]+\s*)"
)
_WHITESPACE_RE = re.compile(r"\s+")
_SPLIT_RE = re.compile(r"[\r\n;,]+")
_WINDOWS_INVALID_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


@dataclass(frozen=True, slots=True)
class CleanedList:
    items: tuple[str, ...]
    duplicates: tuple[str, ...]
    ignored: tuple[str, ...]


def strip_list_prefix(value: str) -> str:
    return _PREFIX_RE.sub("", value, count=1).strip()


def clean_display_name(value: str) -> str:
    value = value.replace("\u200b", "").replace("\ufeff", "")
    return _WHITESPACE_RE.sub(" ", strip_list_prefix(value)).strip(" -\u2013\u2014\t")


def normalize_name(value: str) -> str:
    cleaned = clean_display_name(value).casefold()
    decomposed = unicodedata.normalize("NFKD", cleaned)
    without_accents = "".join(char for char in decomposed if not unicodedata.combining(char))
    return _WHITESPACE_RE.sub(" ", re.sub(r"[^a-z0-9]+", " ", without_accents)).strip()


def parse_name_list(raw: str, *, remove_duplicates: bool = True) -> CleanedList:
    items: list[str] = []
    duplicates: list[str] = []
    ignored: list[str] = []
    seen: set[str] = set()
    for chunk in _SPLIT_RE.split(raw):
        cleaned = clean_display_name(chunk)
        if not cleaned:
            if chunk.strip():
                ignored.append(chunk.strip())
            continue
        key = normalize_name(cleaned)
        if not key:
            ignored.append(chunk.strip())
            continue
        if key in seen:
            duplicates.append(cleaned)
            if remove_duplicates:
                continue
        seen.add(key)
        items.append(cleaned)
    return CleanedList(tuple(items), tuple(duplicates), tuple(ignored))


def sanitize_filename(value: str, *, fallback: str = "sem-nome", max_length: int = 180) -> str:
    name = _WINDOWS_INVALID_RE.sub("_", clean_display_name(value)).rstrip(" .")
    if not name:
        name = fallback
    stem = name.split(".", 1)[0].upper()
    if stem in _RESERVED_NAMES:
        name = f"_{name}"
    return name[:max_length].rstrip(" .") or fallback
