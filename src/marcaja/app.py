"""Ponto de entrada Toga / Briefcase do MarcaJá."""

from __future__ import annotations

import toga
from toga.style import Pack


def _build_main(app: toga.App) -> toga.Widget:
    """Tela principal (Fase 1) — alinhada a 01-UI-SPEC.md."""
    title = toga.Label(
        "MarcaJá",
        style=Pack(font_size=20, font_weight="bold"),
    )
    body = toga.Label(
        "Em breve: lote e marca d'água.",
        style=Pack(flex=1),
    )
    footer = toga.Box(
        children=[
            toga.Button("Ok", on_press=lambda _: None),
            toga.Button("Sair", on_press=lambda _: app.exit()),
        ],
        direction="row",
        style=Pack(gap=8),
    )
    return toga.Box(
        children=[title, body, footer],
        direction="column",
        style=Pack(margin=16, gap=16),
    )


def main() -> toga.App:
    return toga.App(
        formal_name="MarcaJá",
        app_id="dev.marcaja.marcaja",
        startup=_build_main,
    )


if __name__ == "__main__":
    main().main_loop()
