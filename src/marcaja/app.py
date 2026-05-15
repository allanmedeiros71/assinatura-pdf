"""Ponto de entrada Toga / Briefcase do MarcaJá."""

from __future__ import annotations

import toga
from toga.style import Pack


def _quit_app(app: toga.App) -> None:
    """Encerra o app. No Android, ``App.exit()`` do Toga 0.5 é no-op; usa a Activity."""
    native = getattr(getattr(app, "_impl", None), "native", None)
    if native is not None and hasattr(native, "finish"):
        native.finish()
    else:
        app.exit()


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
            toga.Button("Sair", on_press=lambda _: _quit_app(app)),
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
