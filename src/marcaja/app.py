"""Ponto de entrada Toga / Briefcase do MarcaJá."""

from __future__ import annotations

import toga
from toga.style import Pack
from toga.validators import MaxLength

from marcaja.session import Session, truncate_display_name

WATERMARK_MAX = 200


def _quit_app(app: toga.App) -> None:
    """Encerra o app. No Android, ``App.exit()`` do Toga 0.5 é no-op; usa a Activity."""
    native = getattr(getattr(app, "_impl", None), "native", None)
    if native is not None and hasattr(native, "finish"):
        native.finish()
    else:
        app.exit()


class MarcajaApp(toga.App):
    """App principal — Fase 2: sessão, lista e texto da marca."""

    def startup(self) -> None:
        self.session = Session()

        self._empty_label = toga.Label(
            "Nenhum arquivo selecionado",
            style=Pack(flex=1),
        )
        self._file_list = toga.DetailedList(
            data=[],
            accessors=("title", "subtitle", "icon"),
            primary_action="Remover",
            secondary_action=None,
            on_primary_action=self._on_remove_file,
            style=Pack(flex=1),
        )
        self._list_stack = toga.Box(
            children=[self._empty_label, self._file_list],
            style=Pack(flex=1, direction="column"),
        )

        self._watermark_input = toga.MultilineTextInput(
            placeholder="Uso exclusivo — João Silva — maio/2026",
            validators=[MaxLength(WATERMARK_MAX)],
            on_change=self._on_watermark_change,
            style=Pack(height=100),
        )
        self._counter_label = toga.Label(
            "0/200",
            style=Pack(text_align="right"),
        )

        root = toga.Box(
            children=[
                toga.Label(
                    "MarcaJá",
                    style=Pack(font_size=20, font_weight="bold"),
                ),
                toga.Button(
                    "Adicionar PDF ou imagem",
                    on_press=self._on_add_files,
                ),
                self._list_stack,
                toga.Label("Marca d'água"),
                self._watermark_input,
                self._counter_label,
                toga.Box(
                    children=[
                        toga.Button("Ok", on_press=self._on_ok),
                        toga.Button(
                            "Sair",
                            on_press=lambda _: _quit_app(self),
                        ),
                    ],
                    style=Pack(direction="row", gap=8),
                ),
            ],
            style=Pack(margin=16, gap=16, direction="column"),
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = root
        self._refresh_file_list()
        self._update_counter()

    def _refresh_file_list(self) -> None:
        if self.session.is_empty():
            self._list_stack.children = [self._empty_label]
        else:
            self._file_list.data = [
                {
                    "title": truncate_display_name(entry.display_name),
                    "subtitle": entry.kind,
                    "icon": "",
                    "path": str(entry.path),
                }
                for entry in self.session.entries
            ]
            self._list_stack.children = [self._file_list]

    def _update_counter(self) -> None:
        n = len(self.session.watermark_text)
        self._counter_label.text = f"{n}/{WATERMARK_MAX}"

    def _on_watermark_change(self, widget: toga.MultilineTextInput) -> None:
        text = widget.value or ""
        if len(text) > WATERMARK_MAX:
            text = text[:WATERMARK_MAX]
            widget.value = text
        self.session.watermark_text = text
        self._update_counter()

    async def _on_add_files(self, widget: toga.Widget) -> None:
        dialog = toga.OpenFileDialog(
            title="Selecionar arquivos",
            file_types=["pdf", "png", "jpg", "jpeg"],
            multiple_select=True,
        )
        result = await self.main_window.dialog(dialog)
        if result is None:
            return
        paths = result if isinstance(result, list) else [result]
        self.session.add_paths(paths)
        self._refresh_file_list()

    def _on_remove_file(self, widget: toga.DetailedList, row: object, **kwargs: object) -> None:
        path_value = getattr(row, "path", None)
        if path_value is None:
            return
        for index, entry in enumerate(self.session.entries):
            if str(entry.path) == str(path_value):
                self.session.remove_at(index)
                break
        self._refresh_file_list()

    async def _on_ok(self, widget: toga.Widget) -> None:
        if self.session.is_empty():
            await self.main_window.dialog(
                toga.ErrorDialog(
                    title="Arquivos necessários",
                    message="Adicione pelo menos um arquivo para continuar.",
                )
            )
            return
        if not self.session.watermark_text.strip():
            await self.main_window.dialog(
                toga.ErrorDialog(
                    title="Marca d'água",
                    message="Informe o texto da marca d'água.",
                )
            )
            return
        await self.main_window.dialog(
            toga.InfoDialog(
                title="MarcaJá",
                message=(
                    "Tudo certo com o lote e o texto. "
                    "O processamento dos arquivos virá na próxima etapa."
                ),
            )
        )


def main() -> toga.App:
    return MarcajaApp(
        formal_name="MarcaJá",
        app_id="dev.marcaja.marcaja",
    )


if __name__ == "__main__":
    main().main_loop()
