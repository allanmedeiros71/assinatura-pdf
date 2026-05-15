# Phase 2: Sessão, lista e texto da marca - Context

**Gathered:** 2026-05-15  
**Status:** Ready for planning  

<domain>
## Phase Boundary

Na **mesma** `MainWindow` da Fase 1, o usuário **compõe o lote**: seleciona múltiplos PDFs/imagens, vê a lista, remove entradas, digita o texto da marca (≤200 caracteres) com feedback claro. Estado de sessão em memória (sem pipeline PDF).

**Cobre:** FILE-01, FILE-02, FILE-03, WM-01, WM-02.

**Fora desta fase:** processamento de PDF, marca diagonal, cache de jobs, progresso de lote, compartilhar/salvar, endurecimento (fases 3–5). O botão **Ok** valida e informa; **não** gera arquivos de saída nesta fase.

</domain>

<decisions>
## Implementation Decisions

### Layout da tela única (UI-01, UI-03)
- **D-01:** Ordem vertical após o título **MarcaJá**: botão de adicionar arquivos → **lista** de arquivos → campo **Marca d'água** → faixa fixa **Ok** / **Sair** (substitui o placeholder central da Fase 1).
- **D-02:** A lista ocupa a **área central flexível** (`flex=1`) com **rolagem** interna; **Ok** e **Sair** permanecem sempre visíveis na parte inferior sem rolagem da tela inteira.
- **D-03:** Estado vazio da lista: mensagem curta em pt-BR, ex.: *"Nenhum arquivo selecionado"*, na área da lista (além do botão de adicionar).
- **D-04:** Rótulo do campo de texto: **"Marca d'água"** (não usar rótulo longo "Texto da marca d'água").

### Adicionar arquivos (FILE-01)
- **D-05:** Botão que abre o seletor do sistema: rótulo **"Adicionar PDF ou imagem"**.
- **D-06:** Nova seleção **acumula** entradas na lista; não substitui o lote anterior.
- **D-07:** Filtros do seletor: **PDF, PNG e JPEG** apenas (extensões/MIME conforme suporte Toga/Android no plano).
- **D-08:** Cancelar o seletor: **sem alteração** na lista e **sem** mensagem ao usuário.

### Lista editável (FILE-02, FILE-03)
- **D-09:** Cada linha mostra **nome do arquivo + tipo** (ex.: sufixo ou etiqueta **PDF**, **PNG**, **JPEG**) para distinguir entradas.
- **D-10:** Remoção por **botão explícito por linha** (rótulo **"Remover"** e/ou ícone de lixeira — detalhe no plano/UI-SPEC).
- **D-11:** Se o mesmo arquivo for adicionado de novo: **ignorar silenciosamente** (sem duplicata na lista).
- **D-12:** Nomes longos: **truncar com reticências** na linha.

### Campo da marca (WM-01, WM-02)
- **D-13:** Limite de **200 caracteres**: **bloquear** digitação além do limite (não depender só de truncar ao digitar).
- **D-14:** Contador **"N/200"** visível, alinhado à **direita** abaixo ou ao lado do campo.
- **D-15:** Campo **multilinha** (cerca de **2–4 linhas** visíveis), adequado a textos longos dentro do limite.
- **D-16:** Placeholder de exemplo (quando vazio): *"Uso exclusivo — João Silva — maio/2026"* (tom orientativo; microcopy fino no plano).

### Botão Ok nesta fase (sem processamento)
- **D-17:** Ao tocar **Ok**: **validar** lote e texto; erros em **diálogo** curto pt-BR (Toga `ErrorDialog` ou equivalente).
- **D-18:** **Sem arquivos** na lista → mensagem pedindo adicionar pelo menos um arquivo.
- **D-19:** **Texto da marca vazio** (com arquivos presentes) → mensagem de que o texto é **obrigatório**.
- **D-20:** Se validação passar → diálogo informativo curto de que o **processamento virá na próxima etapa** (honesto; sem simular export nesta fase).

### Arquitetura e integração (carry-over Fase 1)
- **D-21:** Manter **uma** `MainWindow`, pt-BR, Material/Toga, botões **Ok** (primário) e **Sair** (encerra via `_quit_app` / padrão Fase 1).
- **D-22:** Estado de sessão (paths da lista + texto da marca) em módulo dedicado (ex.: `session.py`), conforme `.planning/research/ARCHITECTURE.md` — único sítio da verdade para o lote.

### Claude's Discretion
- Widgets Toga concretos (`Table` vs `ScrollContainer` + linhas customizadas), espaçamento dp alinhado a `01-UI-SPEC.md`.
- Textos exatos dos diálogos de erro e do diálogo de sucesso parcial (D-20).
- Tratamento de colagem >200 caracteres na prática do widget (desde que o comportamento observável respeite D-13 e D-14).
- Normalização de paths/URIs retornados pelo `OpenFileDialog` no Android.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Fase e requisitos
- `.planning/ROADMAP.md` — Fase 2: meta, critérios de sucesso, requisitos FILE-01–03, WM-01–02.
- `.planning/REQUIREMENTS.md` — FILE-01, FILE-02, FILE-03, WM-01, WM-02.
- `.planning/PROJECT.md` — produto, marco v1.0, decisões-chave.
- `projeto.md` — dois campos (arquivos + texto), multi-upload, 200 caracteres.

### Fase anterior (UI e shell)
- `.planning/phases/01-fundacao-beeware-tela-principal/01-CONTEXT.md` — tela única, Ok/Sair, pt-BR, placeholder substituível.
- `.planning/phases/01-fundacao-beeware-tela-principal/01-UI-SPEC.md` — escala dp, tipografia, Ok primário, hierarquia Material.

### Pesquisa e arquitetura
- `.planning/research/ARCHITECTURE.md` — `session.py`, `OpenFileDialog` com `multiple_select=True`, handlers async.
- `.planning/research/STACK.md` — Briefcase/Toga Android.

### Código atual
- `src/marcaja/app.py` — layout Fase 1 a evoluir (placeholder → lista + campo).
- `src/marcaja/__main__.py` — entrada `-m marcaja`.

### Convenções
- `.cursor/rules/language-pt-br.mdc` — pt-BR em cópia de UI e documentação.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/marcaja/app.py` — `_build_main`, `_quit_app` (Sair no Android); footer Ok/Sair já posicionado.
- `pyproject.toml` — `toga-android` no alvo Android; padrão Briefcase estabelecido na Fase 1.

### Established Patterns
- Layout em coluna: título → corpo flex → footer horizontal (Fase 1 / `01-UI-SPEC.md`).
- Strings visíveis em pt-BR; botão **Ok** com semântica de confirmar (evolução agora com validação, sem pipeline).

### Integration Points
- Substituir `body` placeholder por: botão adicionar, lista rolável, `TextInput` multilinha + contador.
- Handlers `async` para `OpenFileDialog` (pesquisa ARCHITECTURE); atualizar widgets a partir de `session.py`.
- **Ok** deixa de ser `lambda _: None` → validação + diálogos (D-17–D-20).

</code_context>

<specifics>
## Specific Ideas

- Alinhado a `projeto.md`: primeiro “campo” = lote de arquivos, segundo = texto da marca.
- Exemplo de placeholder da marca aprovado na discussão (D-16).
- Duplicatas ignoradas sem drama — usuário corrige com Remover se precisar.

</specifics>

<deferred>
## Deferred Ideas

- Processamento em lote ao Ok, geometria diagonal da marca, PDF endurecido, compartilhar/salvar → **Fases 3–5**.
- Diálogo “adicionar vs substituir” lote → não pedido (acumular é a regra).
- Ok desabilitado até formulário válido → rejeitado em favor de validação com diálogo (D-17).

</deferred>

---

*Phase: 2-Sessão, lista e texto da marca*  
*Context gathered: 2026-05-15*
