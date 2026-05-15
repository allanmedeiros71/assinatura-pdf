---
phase: 02
slug: sessao-lista-e-texto-da-marca
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-15
---

# Fase 02 — Estratégia de validação

> Contrato Nyquist para Fase 2. Unit leve em `session.py`; smoke Android manual para picker e UI.

---

## Infraestrutura de testes

| Propriedade | Valor |
|-------------|--------|
| **Framework** | `pytest` (opcional dev) + `compileall` |
| **Arquivo de config** | nenhum obrigatório |
| **Comando rápido** | `python -m compileall -q src/marcaja` |
| **Comando suite** | `pytest -q tests/test_session.py` (quando existir) |
| **Tempo estimado** | &lt; 10 s |

---

## Taxa de amostragem

- **Após tarefa em `src/marcaja`:** `compileall`
- **Após plano 02-01:** `pytest -q tests/test_session.py`
- **Após plano 02-02:** compileall + smoke manual Android
- **Antes de `/gsd-verify-work`:** pytest verde (se Wave 0 criado) + UAT humano

---

## Mapa por tarefa

| Task ID | Plan | Wave | Requirement | Tipo | Comando | Manual |
|---------|------|------|-------------|------|---------|--------|
| 02-01-01 | 02-01 | 1 | FILE-01 (lógica) | unit | `pytest -q tests/test_session.py` | — |
| 02-02-01 | 02-02 | 2 | FILE-01–03, WM-01–02 | compile | `python -m compileall -q src/marcaja` | picker + lista |
| 02-02-02 | 02-02 | 2 | WM-02, D-17–20 | compile + manual | idem | contador, Ok diálogos |

---

## Wave 0

- [ ] `tests/test_session.py` — dedupe, `kind_from_suffix`, `remove_at`
- [ ] `pytest` em `[project.optional-dependencies] dev` se ainda ausente (somente se necessário para CI local)

---

## Somente manual

| Comportamento | Requirement | Por quê | Passos |
|---------------|-------------|---------|--------|
| OpenFileDialog multi no Android | FILE-01 | Depende do SO | Adicionar 2+ arquivos; ver lista |
| Remover linha | FILE-03 | Gestos nativos | Remover um item; lista atualiza |
| Ok validação / info | D-17–20 | Diálogos nativos | Ok sem arquivos; sem texto; com ambos |

---

## Sign-off

- [ ] Tarefas com verify automatizado ou dependência Wave 0
- [ ] `nyquist_compliant: true` após Wave 0 executado

**Aprovação:** pendente
