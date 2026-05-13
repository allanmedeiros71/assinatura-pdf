# Fase 01 — Mapeamento de padrões (MarcaJá)

**Gerado:** 2026-05-12  
**Escopo:** greenfield — sem analogs internos.

## Resumo

| Papel | Analog mais próximo | Evidência |
|-------|---------------------|-----------|
| Estrutura Briefcase/Toga | Tutorial oficial BeeWare / `briefcase new` (referência conceitual) | STACK.md, documentação Briefcase |
| Layout Android Material | `01-UI-SPEC.md` | Contrato de UI aprovado |

## Arquivos novos (Fase 1)

| Caminho | Função |
|---------|--------|
| `pyproject.toml` | Metadados PEP 621 + `[tool.briefcase]` |
| `src/marcaja/app.py` | `toga.App`, `MainWindow`, widgets |
| `src/marcaja/__init__.py` | Pacote Python |
| `src/marcaja/resources/fonts/*.ttf` | Liberation Sans (WM-07) |

## Notas

- Não há código legado no repositório para copiar; seguir pins de `.planning/research/STACK.md`.

---

## PATTERN MAPPING COMPLETE
