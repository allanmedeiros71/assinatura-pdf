"""Estado da sessão de lote (Fase 2)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ALLOWED_SUFFIXES = frozenset({".pdf", ".png", ".jpg", ".jpeg"})

MAX_DISPLAY_NAME_LEN = 40


def kind_from_path(path: Path | str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        return "PDF"
    if suffix == ".png":
        return "PNG"
    if suffix in {".jpg", ".jpeg"}:
        return "JPEG"
    raise ValueError(f"extensão não suportada: {suffix}")


def truncate_display_name(name: str, max_len: int = MAX_DISPLAY_NAME_LEN) -> str:
    if len(name) <= max_len:
        return name
    return name[: max_len - 1] + "…"


@dataclass(frozen=True)
class FileEntry:
    path: Path
    display_name: str
    kind: str


class Session:
    def __init__(self) -> None:
        self._entries: list[FileEntry] = []
        self._keys: set[str] = set()
        self.watermark_text: str = ""

    @property
    def entries(self) -> tuple[FileEntry, ...]:
        return tuple(self._entries)

    def is_empty(self) -> bool:
        return not self._entries

    def _normalize_key(self, path: Path | str) -> str:
        p = Path(path)
        try:
            return str(p.resolve())
        except OSError:
            return str(p)

    def add_paths(self, paths: Iterable[Path | str]) -> int:
        added = 0
        for raw in paths:
            path = Path(raw)
            suffix = path.suffix.lower()
            if suffix not in ALLOWED_SUFFIXES:
                continue
            key = self._normalize_key(path)
            if key in self._keys:
                continue
            entry = FileEntry(
                path=path,
                display_name=path.name,
                kind=kind_from_path(path),
            )
            self._entries.append(entry)
            self._keys.add(key)
            added += 1
        return added

    def remove_at(self, index: int) -> None:
        if index < 0 or index >= len(self._entries):
            raise IndexError(index)
        entry = self._entries.pop(index)
        self._keys.discard(self._normalize_key(entry.path))
