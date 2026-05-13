---
phase: 01
slug: fundacao-beeware-tela-principal
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-05-12
---

# Fase 01 — Estratégia de validação

> Contrato de validação Nyquist para a Fase 1. Automatização mínima (Python); smoke Android manual.

---

## Infraestrutura de testes

| Propriedade | Valor |
|-------------|--------|
| **Framework** | *(sem pytest obrigatório na Fase 1)* — `compileall` como gate leve |
| **Arquivo de config** | nenhum |
| **Comando rápido** | `python -m compileall -q src/marcaja` |
| **Comando suite completa** | igual ao rápido até introdução de `pytest` |
| **Tempo estimado** | &lt; 5 s |

---

## Taxa de amostragem

- **Após cada tarefa com alteração em `src/marcaja`:** `python -m compileall -q src/marcaja`
- **Após onda com UI:** smoke manual `briefcase run android` quando ambiente disponível
- **Antes de `/gsd-verify-work`:** compileall verde + smoke manual registrado na UAT quando aplicável

---

## Mapa por tarefa (resumo)

| Task ID | Plan | Wave | Requirement | Tipo | Comando automatizado | Manual |
|---------|------|------|-------------|------|----------------------|--------|
| 01-01-01 | 01-01 | 1 | PLAT-01 | compile | `python -m compileall -q src/marcaja` | — |
| 01-01-02 | 01-01 | 1 | PLAT-01 | compile | idem | briefcase opcional |
| 01-02-01 | 01-02 | 2 | UI-01–03 | compile + manual | idem | ver UI-SPEC |
| 01-02-02 | 01-02 | 2 | WM-07 | arquivo | `test -f src/marcaja/resources/fonts/LiberationSans-Regular.ttf` | licença no README |

---

## Wave 0

- *Não exigido para esta fase* — gate leve é `compileall`; pytest pode ser adicionado em fase posterior.

---

## Verificações só manuais

| Comportamento | Requirement | Por que manual | Instruções |
|---------------|-------------|----------------|-------------|
| App abre no Android com tela única e botões Ok/Sair | UI-01–03 | Emulador/dispositivo | `briefcase run android`; confirmar layout conforme `01-UI-SPEC.md` |
| Sair encerra o app | D-05 | ciclo de vida | Toque em **Sair**; app deve fechar |

---

## Sign-off

- [x] Tarefas têm verificação automatizada ou dependência Wave 0 N/A
- [x] Continuidade de amostragem: compileall após mudanças Python
- [ ] `nyquist_compliant: true` após primeira execução verificada

**Aprovação:** pendente até primeira execução da fase
