---
phase: 02-sessao-lista-e-texto-da-marca
plan: "02"
subsystem: ui
tags: [toga, OpenFileDialog, DetailedList, MultilineTextInput]

requires:
  - phase: 02-sessao-lista-e-texto-da-marca
    plan: "01"
    provides: Session e testes
provides:
  - "MainWindow Fase 2 com picker, lista, marca 200 chars, Ok validado"
affects:
  - "03"

tech-stack:
  added: []
  patterns:
    - "MarcajaApp(toga.App) com handlers async para diálogos"
    - "DetailedList primary_action Remover"

key-files:
  created: []
  modified:
    - src/marcaja/app.py

key-decisions:
  - "Estado vazio alterna children do _list_stack (sem .hidden)"
  - "path em cada row da DetailedList para remoção"

patterns-established:
  - "OpenFileDialog multiple_select + file_types pdf/png/jpg/jpeg"

requirements-completed: [FILE-01, FILE-02, FILE-03, WM-01, WM-02]

duration: 15min
completed: 2026-05-15
---

# Fase 2 — Resumo do plano 02-02

**UI integrada à sessão: adicionar arquivos, lista com Remover, campo Marca d'água com contador e Ok com diálogos de validação (sem processar PDF).**

## Accomplishments

- Botão **Adicionar PDF ou imagem** com `OpenFileDialog` multi.
- Lista `DetailedList` + mensagem de vazio.
- `MultilineTextInput` + `MaxLength(200)` + contador N/200.
- **Ok** → erros ou `InfoDialog` de próxima etapa; **Sair** via `_quit_app`.

## Verification

- `python -m compileall -q src/marcaja`
- Smoke manual Android pendente (UAT)
