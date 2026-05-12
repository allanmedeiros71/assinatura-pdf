# MarcaJá

## What This Is

App Android **100% local** (sem servidor e sem login) para o usuário enviar **PDFs e imagens**, informar um **texto de marca d'água** (até 200 caracteres) e receber de volta **arquivos PDF** com a marca aplicada, prontos para compartilhar com seguradoras, bancos, concessionárias etc., reduzindo risco de uso indevido do documento original.

## Core Value

O usuário consegue, em **uma única tela**, marcar **vários arquivos de uma vez** e **baixar PDFs** com marca d'água visível e **proteção forte contra cópia de texto** (e sem camada OCR útil), no próprio smartphone.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Uma tela única ao abrir o app (Material/Android moderno).
- [ ] Upload de **múltiplos** PDFs e/ou imagens por vez.
- [ ] Campo de texto da marca (até **200** caracteres).
- [ ] Botões **Ok** (processar) e **Sair**.
- [ ] Ao confirmar: aplicar marca d'água com o texto informado e disponibilizar **download** dos resultados.
- [ ] Marca d'água: **ângulo** alinhado à diagonal canto inferior esquerdo → canto superior direito; **tamanho de fonte** proporcional à diagonal; quebra em **várias linhas** se necessário para legibilidade.
- [ ] Fonte **Arial ou equivalente open source** (ex. Liberation Sans, Arimo).
- [ ] Saída sempre **PDF**; texto **não copiável**; **remover/suprimir OCR** nos PDFs gerados.
- [ ] Implementação em **Python** com **BeeWare** (app nativo Android).

### Out of Scope

- **Autenticação / contas** — app local, sem backend.
- **Auditoria e logs persistentes** — não requerido.
- **RBAC / perfis** — não requerido.
- **Regras de negócio adicionais** — nenhuma além do fluxo acima.
- **Versões iOS/desktop** — não especificado; foco Android conforme especificação.

## Context

- Uso típico: anexar documentos sensíveis a **terceiros**; marca d'água identifica destino/contexto e desencoraja reuso.
- Entrada: PDF e imagens (ex. capturas de tela).
- Processamento e armazenamento temporário **no dispositivo**; sem nuvem implícita na especificação.

## Constraints

- **Stack:** Python + BeeWare (Briefcase/Toga) para Android.
- **UX:** padrões Android atuais (Material).
- **Segurança de PDF:** saída com restrições de cópia e **sem OCR** — implica escolhas técnicas cuidadosas (rasterização vs. texto real, metadados de texto acessível, etc.).
- **Performance:** aceitável em smartphone para lotes pequenos/médios (tamanho típico de anexos pessoais).

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| BeeWare para Android | Requisito explícito do documento de ideia | — Pending |
| Saída sempre PDF endurecido | Reduz extração trivial de texto vs. imagem pura | — Pending |
| Sem backend | Requisito de privacidade e simplicidade | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):

1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):

1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-12 after normalizing documentation to pt-BR*
