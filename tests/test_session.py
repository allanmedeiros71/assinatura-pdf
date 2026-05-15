"""Testes do modelo de sessão."""

from pathlib import Path

import pytest

from marcaja.session import Session, kind_from_path


def test_add_paths_accumulates(tmp_path: Path) -> None:
    session = Session()
    a = tmp_path / "a.pdf"
    b = tmp_path / "b.png"
    a.write_bytes(b"%PDF")
    b.write_bytes(b"\x89PNG")

    assert session.add_paths([a, b]) == 2
    assert len(session.entries) == 2


def test_duplicate_ignored(tmp_path: Path) -> None:
    session = Session()
    f = tmp_path / "doc.pdf"
    f.write_bytes(b"%PDF")

    assert session.add_paths([f]) == 1
    assert session.add_paths([f]) == 0
    assert len(session.entries) == 1


def test_remove_at(tmp_path: Path) -> None:
    session = Session()
    a = tmp_path / "a.pdf"
    b = tmp_path / "b.png"
    a.write_bytes(b"x")
    b.write_bytes(b"y")
    session.add_paths([a, b])

    session.remove_at(0)
    assert len(session.entries) == 1
    assert session.entries[0].path == b


def test_txt_ignored(tmp_path: Path) -> None:
    session = Session()
    t = tmp_path / "note.txt"
    t.write_text("x")

    assert session.add_paths([t]) == 0
    assert session.is_empty()


def test_kind_from_path() -> None:
    assert kind_from_path("x.pdf") == "PDF"
    assert kind_from_path("x.png") == "PNG"
    assert kind_from_path("x.jpg") == "JPEG"
    assert kind_from_path("x.jpeg") == "JPEG"
