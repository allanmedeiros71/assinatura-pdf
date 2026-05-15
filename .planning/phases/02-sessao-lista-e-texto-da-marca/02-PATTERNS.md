# Fase 02 — Mapeamento de padrões (MarcaJá)

**Gerado:** 2026-05-15

## Analogs internos

| Papel | Analog | Evidência |
|-------|--------|-----------|
| Layout coluna + footer | `src/marcaja/app.py` `_build_main` | Fase 1 — título, corpo flex, Ok/Sair |
| Encerrar Android | `_quit_app` em `app.py` | `native.finish()` |
| Tokens UI | `01-UI-SPEC.md` | margin 16, gap 16, font_size 20 título |
| Estado futuro | `.planning/research/ARCHITECTURE.md` | `session.py` prescrito |

## Arquivos novos / modificados

| Caminho | Função |
|---------|--------|
| `src/marcaja/session.py` | Lote em memória, dedupe, tipos |
| `src/marcaja/app.py` | `toga.App` + UI Fase 2 + handlers async |
| `tests/test_session.py` | Dedupe, kind, remove (Wave 0 leve) |

## Padrão a seguir

- Refatorar para **subclasse** `toga.App` com `self.session` e `self.main_window` (handlers `async` para diálogos).
- Manter `main()` como factory para Briefcase.
- Strings pt-BR conforme `02-UI-SPEC.md`.

---

## PATTERN MAPPING COMPLETE
