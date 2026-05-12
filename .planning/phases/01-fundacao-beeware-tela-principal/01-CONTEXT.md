# Phase 1: Fundação BeeWare e tela principal - Context

**Gathered:** 2026-05-12  
**Status:** Ready for planning  

**Nota:** Discuss-phase executada em modo **compacto** (sem `gsd-sdk` / sem seleção interativa de áreas cinzentas). As decisões abaixo alinham `PROJECT.md`, `REQUIREMENTS.md`, `projeto.md`, `.planning/research/STACK.md` e a regra de idioma pt-BR. Ajustes finos ficam para `/gsd-plan-phase 1`.

<domain>
## Phase Boundary

Entregar o **esqueleto BeeWare no Android**: projeto Briefcase/Toga funcional, **uma** `MainWindow`, aparência compatível com **Material/Android moderno**, botões **Ok** e **Sair** visíveis, e a **fonte open source** (equivalente Arial) **presente no repositório** com licença documentada — cobrindo **PLAT-01**, **UI-01**, **UI-02**, **UI-03**, **WM-07**.  
**Fora desta fase:** seleção de arquivos, campo de texto da marca, pipeline PDF, progresso de lote (fases 2–5).

</domain>

<decisions>
## Implementation Decisions

### Projeto Briefcase / identidade
- **D-01:** Criar o app BeeWare com nome/slug **`marcaja`** (alinhado a `.planning/research/ARCHITECTURE.md` e código `MARCAJA` em `.planning/config.json`), em **Python 3.12** conforme pesquisa de stack.
- **D-02:** Plataforma inicial: **Android** via Briefcase; validar `briefcase dev` / `briefcase run android` no fluxo documentado no plano.

### UI e idioma
- **D-03:** Todas as **strings visíveis ao usuário** em **português do Brasil (pt-BR)**, conforme `.cursor/rules/language-pt-br.mdc`.
- **D-04:** **Uma** tela principal sem onboarding (**UI-01**). Layout inicial: **título** "MarcaJá" no topo; área central pode ser **placeholder** (vazia ou texto curto) até a Fase 2; **Ok** e **Sair** **visíveis** na parte inferior (**UI-03**), estilo coerente com **Toga no Android** / sensação Material (**UI-02**) — detalhe de widgets fica ao plano.
- **D-05:** **Sair** encerra o aplicativo de forma correta no ciclo de vida Android (padrão Toga/Briefcase; implementação concreta no plano).

### Fonte (WM-07)
- **D-06:** Incorporar **Liberation Sans** (`.ttf`) como equivalente open source a Arial, licença **OFL**: arquivos sob caminho estável (ex.: `resources/fonts/` ou equivalente gerado pelo Briefcase) **e** referência no **README** ou na tabela **Key Decisions** do `PROJECT.md`.

### Claude's Discretion
- Tokens de cor/spacing exatos do Toga; versões patch de Briefcase/Toga dentro da série recomendada na pesquisa; microcopy dos placeholders da área central.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planeamento e requisitos
- `.planning/ROADMAP.md` — Fase 1: meta, critérios de sucesso, **UI hint**: yes, requisitos mapeados.
- `.planning/PROJECT.md` — produto, marco v1.0, decisões-chave.
- `.planning/REQUIREMENTS.md` — **PLAT-01**, **UI-01**–**UI-03**, **WM-07** (e restante para contexto, sem implementar fora do âncora da fase).
- `.planning/MILESTONES.md` — marco **v1.0 — Execução MVP**.

### Pesquisa e especificação
- `.planning/research/STACK.md` — versões Python/Briefcase/Toga e notas Android.
- `.planning/research/ARCHITECTURE.md` — separação `ui/` vs pipeline (preparação mental; pipeline fora do escopo da Fase 1).
- `projeto.md` — especificação original MarcaJá.

### Convenções do repositório
- `.cursor/rules/language-pt-br.mdc` — pt-BR padrão em documentação e cópia de UI.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- *(Greenfield)* — não há módulos Python/Toga existentes no repositório; reutilizar apenas **templates/padrões** da documentação BeeWare citados em `STACK.md` / `ARCHITECTURE.md`.

### Established Patterns
- Nenhum padrão interno ainda; seguir estrutura sugerida na pesquisa (`MainWindow`, handlers assíncronos nas fases seguintes).

### Integration Points
- Fase 2 ligará lista de arquivos e campo de texto à mesma `MainWindow`; manter API interna simples (ex.: métodos stub no `App` ou módulo `ui/`).

</code_context>

<specifics>
## Specific Ideas

- Nome de produto na barra/título: **MarcaJá**.
- Botões com rótulos **Ok** e **Sair** (como em `projeto.md`).

</specifics>

<deferred>
## Deferred Ideas

- Seleção múltipla de arquivos, lista editável, campo de marca 200 caracteres → **Fase 2**.
- Motor PDF, cache, saída → **Fase 3**.
- Marca diagonal e lote → **Fase 4**.
- Endurecimento PDF e compartilhar/salvar → **Fase 5**.

**Rever opcionalmente na planificação:** se o usuário quiser outro equivalente Arial (**Arimo** em vez de Liberation Sans), trocar antes de fechar o PLAN — impacto baixo na Fase 1.

</deferred>

---

*Phase: 1-Fundação BeeWare e tela principal*  
*Context gathered: 2026-05-12*
