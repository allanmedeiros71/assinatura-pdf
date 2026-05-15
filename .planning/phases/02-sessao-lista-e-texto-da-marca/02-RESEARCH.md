# Fase 2 — Pesquisa técnica (MarcaJá)

**Gerado:** 2026-05-15  
**Fonte:** `02-CONTEXT.md`, `.planning/research/ARCHITECTURE.md`, `src/marcaja/app.py`, Toga 0.5.4 (venv)

## Resumo

A Fase 2 evolui a **mesma MainWindow** da Fase 1: estado de lote em `session.py`, seletor nativo via `OpenFileDialog` (multi), lista editável, campo de marca com limite 200 e **Ok** que valida sem processar PDF.

## Stack (inalterada)

| Peça | Nota |
|------|------|
| Toga | ~=0.5.4 (`toga-android` no APK) |
| Briefcase | 0.4.2 |
| Python | 3.12 |

## Widgets Toga recomendados

| Necessidade | Widget | Evidência |
|-------------|--------|-----------|
| Lista com ação por linha | `toga.DetailedList` | `primary_action` configurável (ex.: **Remover**); `accessors=('title','subtitle',…)` para nome + tipo |
| Área rolável | `toga.ScrollContainer` | Envolver lista ou estado vazio se `DetailedList` não preencher `flex` como esperado |
| Marca multilinha | `toga.MultilineTextInput` | Módulo `toga.widgets.multilinetextinput` |
| Limite 200 | `toga.validators.MaxLength(200)` | Validador oficial; combinar com handler `on_change` para contador **N/200** |
| Picker multi | `toga.OpenFileDialog(..., multiple_select=True, file_types=['pdf','png','jpg','jpeg'])` | `file_types` = extensões **sem** ponto ([dialogs.py](https://github.com/beeware/toga)) |
| Erros / aviso Ok | `toga.ErrorDialog`, `toga.InfoDialog` | `await window.dialog(...)` |
| Encerrar | `_quit_app` existente | Fase 1 — `finish()` no Android |

**Nota:** `toga.TextInput` é linha única; **não** usar para D-15. `SaveFileDialog` **não** é suportado no Android — fora de escopo Fase 2.

## Handlers assíncronos

Padrão ARCHITECTURE + API Toga 0.5:

```python
async def on_add_files(self, widget):
    dialog = toga.OpenFileDialog(
        title="Selecionar arquivos",
        file_types=["pdf", "png", "jpg", "jpeg"],
        multiple_select=True,
    )
    result = await self.main_window.dialog(dialog)
    if result is None:
        return  # D-08: cancelamento silencioso
    # normalizar Path | list[Path] → session.add_files(...)
```

Refatorar `app.py` para subclasse `toga.App` com `startup()` atribuindo `self.main_window` (necessário para `dialog` e refresh da lista).

## session.py (contrato sugerido)

- `FileEntry`: `path: Path`, `display_name: str`, `kind: str` (`PDF` | `PNG` | `JPEG`)
- `Session`: lista ordenada; `add_paths(paths)` acumula, ignora duplicatas por path resolvido; `remove_at(i)`; `watermark_text: str`
- Helpers: `kind_from_suffix(path)`, filtro de extensões permitidas antes de exibir

Paths no Android podem ser `content://` ou caminhos cache — normalizar para `str`/`Path` estável na sessão; detalhe de cópia para cache fica **Fase 3**.

## Riscos

| Risco | Mitigação |
|-------|-----------|
| Comportamento de `OpenFileDialog` no emulador/dispositivo | Smoke manual na UAT; documentar limitações na SUMMARY se picker falhar |
| `DetailedList` vs layout flex | Fallback: `ScrollContainer` + `Box` de linhas (`Label` + `Button` Remover) |
| Colagem >200 no `MultilineTextInput` | `MaxLength(200)` + truncar em `on_change` se widget permitir overflow momentâneo |

## Validation Architecture

| Camada | O quê | Quando |
|--------|--------|--------|
| **Unit** | `tests/test_session.py` — dedupe, kind, remove | Após plano 02-01 |
| **Compile** | `python -m compileall -q src/marcaja` | Após cada tarefa |
| **Manual** | `briefcase run android` — picker, lista, contador, Ok diálogos | UAT Fase 2 |

## Referências

- `.planning/phases/02-sessao-lista-e-texto-da-marca/02-CONTEXT.md`
- `.planning/phases/02-sessao-lista-e-texto-da-marca/02-UI-SPEC.md`
- `.planning/phases/01-fundacao-beeware-tela-principal/01-UI-SPEC.md`
- `src/marcaja/app.py`

---

## RESEARCH COMPLETE
