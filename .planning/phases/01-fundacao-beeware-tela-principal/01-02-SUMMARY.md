---
phase: 01-fundacao-beeware-tela-principal
plan: "02"
subsystem: ui
tags: [toga, android, liberation-sans, pt-br]

requires:
  - phase: "01-01"
    provides: "pyproject.toml e pacote src/marcaja"
provides:
  - "Tela principal: título MarcaJá, placeholder, botões Ok e Sair (Sair encerra)"
  - "LiberationSans-Regular.ttf em src/marcaja/resources/fonts/"
  - "README com OFL, briefcase run android e Python 3.12"
affects:
  - "Fase 2"

tech-stack:
  added: []
  patterns: ["Pack para espaçamento; Box column + row no rodapé"]

key-files:
  created:
    - src/marcaja/resources/fonts/LiberationSans-Regular.ttf
  modified:
    - src/marcaja/app.py
    - README.md
    - .planning/PROJECT.md

key-decisions:
  - "Fonte copiada do pacote fonts-liberation do sistema de build (equivalente ao upstream OFL)"

patterns-established:
  - "Ok como stub sem processamento até a Fase 4"

requirements-completed: [UI-01, UI-02, UI-03, WM-07]

duration: 25min
completed: 2026-05-12
---

# Fase 1 — Resumo do plano 01-02

**Tela única Toga com MarcaJá, placeholder pt-BR, botões Ok/Sair e Sair encerrando o app; Liberation Sans empacotada e citada com OFL no README e em PROJECT.**

## Performance

- **Tarefas:** 3 (tarefas 2 e 3 de documentação unificadas num único commit de artefatos)
- **Commits:** bbfceb9, cb0727d

## Task Commits

1. **Tarefa 1: layout MainWindow** — `bbfceb9`
2. **Tarefas 2–3: fonte + README/PROJECT (inclui instruções Android)** — `cb0727d`

## Deviations from Plan

- **Download remoto do TTF:** rede para raw GitHub falhou ou retornou HTML; a fonte foi **copiada** de `/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf` (mesma família OFL) durante o build no ambiente Linux.

## Issues Encountered

- `pip install toga` em venv com Python 3.14 falhou (PyGObject); validação local limitada a `compileall`. Execução Toga real esperada em máquina com **Python 3.12** e dependências GTK ou via **Briefcase no Android**.

## Next Phase Readiness

Base UI pronta para acrescentar lista de arquivos e campo de texto na **Fase 2**.

---
*Phase: 01-fundacao-beeware-tela-principal · Plan: 02*
