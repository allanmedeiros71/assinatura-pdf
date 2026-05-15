---
phase: 02
slug: sessao-lista-e-texto-da-marca
status: approved
extends: 01-UI-SPEC.md
created: 2026-05-15
platform: android
toolkit: toga-briefcase
---

# Fase 02 — Contrato de UI (MarcaJá)

> Estende `01-UI-SPEC.md` (tokens dp, Material, Ok/Sair). Consome `02-CONTEXT.md` e FILE-01–03, WM-01–02.

---

## Estrutura da tela (D-01, D-02)

Ordem vertical na **mesma** `MainWindow`:

| Região | Conteúdo | Comportamento |
|--------|-----------|----------------|
| Topo | Título **MarcaJá** | Igual Fase 1 |
| Ação | Botão **Adicionar PDF ou imagem** | Abre seletor do sistema (multi) |
| Centro (flex=1) | Lista de arquivos **ou** estado vazio | Rolagem interna; mensagem *"Nenhum arquivo selecionado"* quando vazia (D-03) |
| Marca | Rótulo **Marca d'água** + campo multilinha + contador **N/200** à direita | D-13–D-16 |
| Inferior | **Ok** (primário) + **Sair** | Sempre visíveis (UI-03 carry-over) |

---

## Lista de arquivos (FILE-02, FILE-03)

| Elemento | Regra |
|----------|--------|
| Linha | **Nome** truncado com reticências se longo + **tipo** (PDF / PNG / JPEG) como subtítulo ou sufixo (D-09, D-12) |
| Remover | Controle explícito **Remover** por linha (D-10) |
| Vazio | Texto *"Nenhum arquivo selecionado"* visível na área da lista |

Implementação sugerida: `DetailedList` com `primary_action="Remover"` ou linhas em `ScrollContainer`.

---

## Campo Marca d'água (WM-01, WM-02)

| Elemento | Texto / regra |
|----------|----------------|
| Rótulo | **Marca d'água** |
| Placeholder | *"Uso exclusivo — João Silva — maio/2026"* |
| Limite | 200 caracteres — bloquear além do limite; contador **N/200** alinhado à direita |
| Widget | `MultilineTextInput` (~2–4 linhas visíveis) |

---

## Botão Ok (D-17–D-20)

| Situação | Diálogo (pt-BR) |
|----------|-----------------|
| Lista vazia | Título curto + mensagem pedindo **pelo menos um arquivo** |
| Texto vazio | Mensagem de que o **texto da marca é obrigatório** |
| Válido | `InfoDialog` informando que o **processamento virá na próxima etapa** (sem export) |

Usar `ErrorDialog` para erros; `InfoDialog` para sucesso parcial.

---

## Copy fixa (novos)

| Elemento | String |
|----------|--------|
| Adicionar | **Adicionar PDF ou imagem** |
| Estado vazio lista | **Nenhum arquivo selecionado** |
| Remover (ação) | **Remover** |
| Ok / Sair | **Ok**, **Sair** (inalterados) |

---

## Componentes Toga

| UI | Widget |
|----|--------|
| Adicionar | `toga.Button` |
| Lista | `toga.DetailedList` ou `ScrollContainer` + linhas |
| Marca | `toga.MultilineTextInput` + `toga.Label` contador |
| Diálogos | `OpenFileDialog`, `ErrorDialog`, `InfoDialog` |

---

## Rastreio

| ID | Cobertura |
|----|-----------|
| FILE-01 | Botão + OpenFileDialog multi + tipos pdf/png/jpeg |
| FILE-02 | Lista visível + estado vazio |
| FILE-03 | Remover por linha |
| WM-01 | Campo marca |
| WM-02 | 200 + contador + bloqueio |

---

## UI-SPEC COMPLETE

Contrato pronto para execução da Fase 2.
