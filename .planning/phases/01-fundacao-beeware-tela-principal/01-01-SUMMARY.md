---
phase: 01-fundacao-beeware-tela-principal
plan: "01"
subsystem: ui
tags: [briefcase, toga, beeware, android, pyproject]

requires: []
provides:
  - "pyproject.toml Briefcase com app marcaja (bundle dev.marcaja)"
  - "Pacote src/marcaja com toga.App e startup por callback"
affects:
  - "01-02"

tech-stack:
  added: ["toga~=0.5.4", "briefcase==0.4.2 (dev)"]
  patterns: ["toga.App com parâmetro startup retornando raiz de widgets"]

key-files:
  created:
    - pyproject.toml
    - src/marcaja/__init__.py
    - src/marcaja/app.py
  modified: []

key-decisions:
  - "Build backend briefcase.build:build_backend conforme template BeeWare"

patterns-established:
  - "main() retorna toga.App; conteúdo da janela principal via callback startup(app) -> Widget"

requirements-completed: [PLAT-01]

duration: 15min
completed: 2026-05-12
---

# Fase 1 — Resumo do plano 01-01

**Projeto BeeWare `marcaja` criado na raiz com `pyproject.toml` e pacote `src/marcaja` expondo `main()` e `toga.App` com startup mínimo.**

## Performance

- **Tarefas:** 2
- **Commits:** 85e789a, 6d0dab3

## Accomplishments

- Metadados PEP 621 + `[tool.briefcase.app.marcaja]` com `sources = ["src/marcaja"]` e `bundle = "dev.marcaja"`.
- App Toga instanciável com callback de startup e `compileall` verde.

## Task Commits

1. **Tarefa 1: pyproject.toml** — `85e789a`
2. **Tarefa 2: pacote e app** — `6d0dab3`

## Deviations from Plan

Nenhuma — plano seguido.

## Issues Encountered

Nenhum.

## Next Phase Readiness

Pronto para o plano **01-02** (UI-SPEC, fonte, README).

---
*Phase: 01-fundacao-beeware-tela-principal · Plan: 01*
