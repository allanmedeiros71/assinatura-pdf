---
phase: 01
slug: fundacao-beeware-tela-principal
status: human_needed
created: 2026-05-12
---

# Verificação — Fase 1: Fundação BeeWare e tela principal

## Resumo

| Dimensão | Resultado |
|----------|------------|
| Artefatos no repositório | **PASS** — `pyproject.toml`, `src/marcaja/app.py`, fonte TTF, README |
| Sintaxe Python | **PASS** — `python -m compileall -q src/marcaja` |
| Critérios no dispositivo Android | **Pendente humano** — emulador/dispositivo com Briefcase |

## Must-haves do roadmap (checagem)

1. **Instalar e abrir no Android** — requer `briefcase run android` (ou fluxo equivalente) em máquina com SDK; não executado neste ambiente CI.
2. **Uma única tela sem onboarding** — implementado em código (`startup` define um único conteúdo).
3. **Material / Android moderno** — delegado ao backend Toga no dispositivo; confirmação visual **manual**.
4. **Ok e Sair visíveis** — `app.py` contém botões com esses rótulos.
5. **Fonte open source documentada** — Liberation Sans + OFL no README e `PROJECT.md`; ficheiro em `src/marcaja/resources/fonts/`.

## human_verification

- Abrir o app no Android (emulador ou físico) e confirmar: título **MarcaJá**, placeholder, **Ok** e **Sair** na parte inferior, **Sair** fecha o app.
- Confirmar aparência aceitável como UI Android (Material coerente via Toga).

## Gaps

Nenhum gap de implementação identificado no código entregue; apenas evidência em dispositivo.

---

**Veredito:** `human_needed` — aprovar após smoke Android ou reportar issues.
