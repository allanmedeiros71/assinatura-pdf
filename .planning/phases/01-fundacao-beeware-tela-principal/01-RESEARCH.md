# Fase 1 — Pesquisa técnica (MarcaJá)

**Gerado:** 2026-05-12  
**Fonte:** `.planning/research/STACK.md`, `ARCHITECTURE.md`, `PITFALLS.md`, `01-CONTEXT.md`

## Resumo

A Fase 1 entrega o **esqueleto BeeWare**: `pyproject.toml` + app Toga `marcaja`, alvo **Android Gradle** via Briefcase **0.4.2**, Toga **0.5.4**, Python **3.12** no `requires-python`, sem pipeline PDF (Fase 3+).

## Stack prescritiva

| Peça | Versão / nota |
|------|----------------|
| Python | 3.12.x (`requires-python` alinhado a Chaquopy/Briefcase) |
| Toga | ~=0.5.4 |
| Briefcase | 0.4.2 (dev / build) |
| UI | `MainWindow`, `toga.Box`, `toga.Label`, `toga.Button` — backend Android nativo |
| Identificador | App Python `marcaja`; `bundle` reverse-DNS sob `dev.marcaja` + app name |

## Riscos (PITFALLS / STACK)

- Build Android exige **JDK 17**, **ANDROID_HOME**, Python no PATH compatível com `buildPython` Chaquopy quando houver extensões nativas (Fase 3+).
- **Não** bloquear Fase 1 em PyMuPDF — fora de escopo até validação na Fase 3.

## Estrutura de código recomendada (Fase 1 mínimo)

```
pyproject.toml
src/marcaja/
  __init__.py
  app.py          # toga.App + startup
  resources/
    fonts/        # Liberation Sans TTF (WM-07)
```

Módulos `ui/`, `session.py`, `pipeline/` podem ser **stubs** ou omitidos na Fase 1 se o plano consolidar tudo em `app.py` para reduzir superfície; a Fase 2 introduz lista + campo de marca.

## Validation Architecture

Objetivo: feedback rápido durante `/gsd-execute-phase` sem exigir emulador em **cada** commit de tarefa.

| Camada | O quê | Quando |
|--------|--------|--------|
| **Automatizada leve** | `python -m compileall -q src/marcaja` | Após alterações Python |
| **Smoke manual** | `briefcase run android` (ou `briefcase dev android` conforme documentação vigente) | Após onda/plano de UI; requer SDK + dispositivo/emulador |
| **Futuro** | `pytest` em testes de import/layout | Opcional se Wave 0 introduzir testes |

Critério de aceite da fase (produto): ainda depende de verificação humana no dispositivo (ver `ROADMAP` critérios de sucesso) — registrado em `01-VALIDATION.md` como **manual-only** explícito.

## Referências canônicas

- `.planning/research/STACK.md`
- `.planning/research/ARCHITECTURE.md`
- `.planning/phases/01-fundacao-beeware-tela-principal/01-CONTEXT.md`
- `.planning/phases/01-fundacao-beeware-tela-principal/01-UI-SPEC.md`

---

## RESEARCH COMPLETE
