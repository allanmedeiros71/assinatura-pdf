"""Ponto de entrada Toga / Briefcase do MarcaJá."""

from __future__ import annotations

import toga


def _build_placeholder_root(app: toga.App) -> toga.Widget:
    """Conteúdo mínimo até o plano 01-02 aplicar o UI-SPEC completo."""
    return toga.Box(
        children=[
            toga.Label("MarcaJá — em arranque do app."),
        ],
        direction="column",
    )


def main() -> toga.App:
    return toga.App(
        formal_name="MarcaJá",
        app_id="dev.marcaja.marcaja",
        startup=_build_placeholder_root,
    )


if __name__ == "__main__":
    main().main_loop()
