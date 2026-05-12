# Phase 1: Fundação BeeWare e tela principal - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.  
> Decisions are captured in `01-CONTEXT.md`.

**Date:** 2026-05-12  
**Phase:** 1-Fundação BeeWare e tela principal  
**Areas discussed:** Identidade do pacote; UI/idioma; layout mínimo Ok/Sair; fonte OFL; Sair (ciclo de vida)

---

## Identidade do pacote Briefcase

| Option | Description | Selected |
|--------|-------------|----------|
| `marcaja` | Alinhado a pesquisa de arquitetura e `project_code` MARCAJA | ✓ |
| `assinatura_pdf` | Nome legado do repositório | |

**User's choice:** *(implícito — opção recomendada na ausência de discussão interativa)*  
**Notes:** Manter consistência com `.planning/config.json` e pastas futuras.

---

## Idioma da UI

| Option | Description | Selected |
|--------|-------------|----------|
| pt-BR apenas | Regra `.cursor/rules/language-pt-br.mdc` | ✓ |
| pt-BR + en-US para erros | Mais trabalho nesta fase | |

**User's choice:** *(implícito)*  
**Notes:** Mensagens de erro técnicas podem ser tratadas na Fase 5; Fase 1 só precisa de cópia mínima.

---

## Fonte equivalente Arial (WM-07)

| Option | Description | Selected |
|--------|-------------|----------|
| Liberation Sans (OFL) | Recomendado em `STACK.md` | ✓ |
| Arimo (OFL) | Alternativa válida | |

**User's choice:** *(implícito — Liberation Sans)*  
**Notes:** Trocar para Arimo ainda na Fase 1 se o plano preferir — baixo custo.

---

## Claude's Discretion

- Detalhe de widgets Toga (box vs scroll), cores primárias default vs customização leve MarcaJá.

## Deferred Ideas

- Ver secção `<deferred>` em `01-CONTEXT.md`.
