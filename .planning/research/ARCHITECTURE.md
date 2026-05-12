# Architecture Research

**Domain:** BeeWare (Toga + Briefcase) — app Android local para marca d’água em PDF/imagens  
**Researched:** 2026-05-12  
**Confidence:** **MEDIUM** — padrões Toga/Briefcase verificados em documentação oficial e Context7; detalhes finais de paridade Material e comportamento exato de `OpenFileDialog`/`SaveFileDialog` no backend Android merecem validação em dispositivo físico.

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Camada de apresentação (Toga)                      │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ MainWindow   │  │ Lista/seleção│  │ TextInput    │  │ Botões       │  │
│  │ (layout      │  │ de arquivos  │  │ (marca ≤200) │  │ Ok / Sair    │  │
│  │  única tela) │  │ (labels/list)│  │              │  │              │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │                 │          │
├─────────┴─────────────────┴─────────────────┴─────────────────┴──────────┤
│              Orquestração de app (handlers async + estado de sessão)    │
│  • Dispara diálogos: OpenFileDialog / SaveFileDialog / ErrorDialog      │
│  • Agenda trabalho CPU-bound fora do loop de UI                         │
│  • Atualiza widgets na thread principal após conclusão                  │
├─────────────────────────────────────────────────────────────────────────┤
│                     Pipeline de processamento (Python)                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────────┐ │
│  │ Validação   │ →  │ Normalização│ →  │ Marca d’água│ →  │ Endurecimento│ │
│  │ entrada     │    │ (PDF/img)   │    │ (layout/    │    │ PDF (raster/ │ │
│  │ e limites   │    │             │    │  fonte)     │    │ OCR, etc.)   │ │
│  └─────────────┘    └─────────────┘    └─────────────┘    └──────────────┘ │
├─────────────────────────────────────────────────────────────────────────┤
│              I/O e ciclo de vida de arquivos (Paths + diálogos)         │
│  app.paths.cache / data  —  arquivos temporários e metadados de job    │
│  URIs/caminhos devolvidos por diálogos  —  leitura cópia para cache      │
│  SaveFileDialog  —  destino escolhido pelo usuário (export)          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|-------------------------|
| **MainWindow + layout** | Uma tela; hierarquia `Box`/`ScrollContainer`; feedback de progresso e erros | Toga `App`, `MainWindow`, widgets nativos Android via backend Toga |
| **Session / job state** | Lista de arquivos selecionados, texto da marca, flags “a processar”, erros por arquivo | Classe ou `dataclass` isolada da UI; sem lógica PDF |
| **Dialog coordinator** | Abrir `OpenFileDialog` (`multiple_select=True`, `file_types` PDF/imagem) e `SaveFileDialog`; tratar cancelamento | `async def` handlers com `await window.dialog(...)` ([Toga dialogs](https://github.com/beeware/toga/blob/main/docs/en/reference/api/application/dialogs.md)) |
| **Processing pipeline** | Transformar cada entrada em PDF endurecido; determinismo e testes | Módulo(s) Python puros onde possível; interface clara `process(in_path, watermark_text) -> out_path` |
| **Temp & workspace** | Copiar/leituras estáveis; nomes únicos; limpeza após sucesso ou abandono | `app.paths.cache` (e subdiretórios criados pela app) — [Toga Paths](https://github.com/beeware/toga/blob/main/docs/en/reference/api/data-representation/paths.md) |
| **Export UX** | Salvar resultado onde o usuário escolher; mensagens claras | `SaveFileDialog` por arquivo ou estratégia em lote (ZIP) — decisão de produto; erros com `ErrorDialog` |
| **Packaging / plataforma** | Gradle, permissões, tema/cores, wheels Android | Briefcase `pyproject.toml`; documentação [Android / Gradle](https://briefcase.readthedocs.io/en/stable/reference/platforms/android/gradle.html) |

## Recommended Project Structure

```
src/
└── <app_name>/                 # nome Briefcase (ex. marcaja)
    ├── app.py                  # App(...), startup, MainWindow
    ├── ui/
    │   └── main_view.py        # construção da árvore de widgets e binding
    ├── session.py              # estado da sessão (arquivos, texto, jobs)
    ├── dialogs.py              # helpers async para open/save (opcional)
    ├── pipeline/
    │   ├── __init__.py
    │   ├── validate.py         # tipos, tamanhos, limites
    │   ├── watermark.py        # geometria diagonal, multilinha, fonte
    │   └── harden_pdf.py       # rasterização / supressão texto-OCR
    └── resources/              # fontes embutidas (ex. Liberation Sans)
```

### Structure Rationale

- **`ui/` vs `pipeline/`:** separa widgets Toga (thread/UI) de código CPU e de arquivos pesados, facilitando testes unitários do pipeline sem emulador.
- **`session.py`:** único sítio para lista de paths e estado do lote; evita duplicar estado nos widgets.
- **`resources/`:** fonte open-source empacotada de forma reprodutível (alinhado ao requisito Arial/equivalente).

## Architectural Patterns

### Pattern 1: Handlers assíncronos + diálogos modais

**What:** Handlers de botões como `async def`; `await self.main_window.dialog(toga.OpenFileDialog(...))` para picker e save.  
**When to use:** Sempre que houver diálogo ou sequência que depende do usuário (recomendado pela documentação Toga).  
**Trade-offs:** Fluxo linear e legível; exige disciplina para não bloquear o loop com trabalho pesado (ver padrão seguinte).

### Pattern 2: Offload de trabalho pesado (CPU / I/O grande)

**What:** O pipeline de PDF não corre no mesmo contexto que atualiza labels; usar `asyncio.to_thread` (ou executor) para `process(...)`, depois `main_window.content.refresh()` / atualização de propriedades na conclusão.  
**When to use:** Lotes e rasterização; mantém a UI responsiva no Android.  
**Trade-offs:** Cuidado com objetos Toga apenas na thread principal; passar paths e dados simples ao worker.

### Pattern 3: Arquivos temporários sob `app.paths.cache`

**What:** Jobs escrevem outputs intermédios e finais em subpastas por job-ID dentro de `app.paths.cache`; limpar ao concluir export ou ao iniciar nova sessão.  
**When to use:** Entradas vindas de content URIs Android podem precisar de cópia estável antes do processamento.  
**Trade-offs:** Disco e gestão de limpeza; evita depender do CWD (anti-pattern documentado na [gestão de arquivos Toga](https://github.com/beeware/toga/blob/main/docs/en/topics/file-management.md)).

## Data Flow

### Fluxo principal (usuário)

```
[Usuário: Adicionar arquivos]
    ↓
OpenFileDialog (multiple_select=True, file_types adequados)
    ↓
Session armazena pathlib.Path / referências devolvidas pelo diálogo
    ↓
[Usuário: edita texto marca + Ok]
    ↓
Para cada entrada: cópia opcional → cache → pipeline → PDF endurecido em cache
    ↓
[Export]
    ↓
SaveFileDialog (por arquivo ou lote) → escrita no destino escolhido
    ↓
UI confirma / lista erros (ErrorDialog + estado na lista)
```

### Fluxo de estado (UI)

```
Session (fonte de verdade)
    ↓ bind one-way
Widgets (lista, campo texto, indicador de progresso)
    ↑ eventos (on_press) → async handlers → atualizam Session e refrescam UI
```

### Key Data Flows

1. **Seleção multi-arquivo:** resultado de `OpenFileDialog` → normalização para paths internos → exibição na lista.
2. **Processamento em lote:** fila explícita ou loop sequencial com cancelamento opcional; cada item produz artefato em `cache/job_id/`.
3. **Export:** leitura do PDF final em cache → stream/copy para path do `SaveFileDialog`; após sucesso, opcionalmente remover temporários desse job.

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|---------------------------|
| Usuário único, lotes pequenos (requisito) | Pipeline sequencial simples; limite explícito de N arquivos ou MB totais na validação. |
| PDFs grandes / muitas páginas | Processar página a página ou documento a documento; liberar buffers; considerar limite de memória e mensagem “arquivo muito grande”. |
| Dependências nativas (PyMuPDF etc.) | Validar cedo wheels Android via Briefcase/Chaquopy; preferir camadas **pure Python** quando possível ou dependências já suportadas no [repositório secundário](https://chaquo.com/pypi-13.1/) referido na documentação Briefcase. |

### Scaling Priorities

1. **First bottleneck:** rasterização / manipulação PDF na thread principal → congela UI; mitigar com offload.
2. **Second bottleneck:** espaço em disco em `cache` → limpeza agressiva e quotas.

## Anti-Patterns

### Anti-Pattern 1: Escrever temporários no diretório de trabalho atual

**What people do:** `open("out.pdf", "wb")` relativo ao CWD.  
**Why it's wrong:** Em Android empacotado o CWD não é fiável; falhas intermitentes e difíceis de reproduzir.  
**Do this instead:** `app.paths.cache` / `app.paths.data` conforme semântica ([Toga Paths](https://github.com/beeware/toga/blob/main/docs/en/reference/api/data-representation/paths.md)).

### Anti-Pattern 2: Misturar widgets Toga dentro do worker do pipeline

**What people do:** Atualizar `Label.text` a partir de `to_thread`.  
**Why it's wrong:** backends GUI esperam mutações na thread principal.  
**Do this instead:** Worker devolve resultados estruturados; handler async aplica mudanças na UI após `await`.

### Anti-Pattern 3: Bloquear a UI à espera de todo o lote antes de feedback

**What people do:** Um único `await` longo sem progresso.  
**Why it's wrong:** Android pode sugerir ANR ou usuário assume crash.  
**Do this instead:** Progresso por arquivo (label ou determinate progress quando disponível) e erros incrementais.

## Integration Points

### External services

| Service | Integration Pattern | Notes |
|---------|---------------------|--------|
| *(nenhum backend)* | — | Requisito de privacidade; toda a lógica local. |
| Play Store / assinatura | Fora do runtime do app | `briefcase package` exige assinatura para artefatos utilizáveis ([documentação Briefcase](https://briefcase.readthedocs.io/en/stable/reference/platforms/android/gradle.html)). |

### Internal boundaries

| Boundary | Communication | Notes |
|----------|---------------|--------|
| UI ↔ Session | chamadas síncronas simples / métodos na mesma thread UI | Mantém modelo mental claro. |
| UI ↔ Pipeline | apenas via offload + mensagens (paths, exceções serializáveis) | Sem imports Toga dentro de `pipeline/`. |
| App ↔ SO Android | Toga dialogs + paths | Permissões extra só se necessário (ex. `permission.photo_library` se aceder à galeria fora do document picker — mapeamento em [Android permissions](https://briefcase.readthedocs.io/en/stable/reference/platforms/android/gradle.html#android-permissions)). |

## Suggested build order for phases

Ordem sugerida para minimizar retrabalho e validar riscos cedo (alinhado a requisitos em `.planning/PROJECT.md`):

1. **Fundação Briefcase + janela única** — `briefcase new`, `MainWindow`, tema/cores Android (`primary_color`, etc.); layout estático com botões e campo de texto vazio. *Desbloqueia:* iteração em dispositivo/emulador.
2. **Modelo de sessão + lista de arquivos** — estado em memória; UI para mostrar/remover itens; sem PDF ainda. *Desbloqueia:* contrato de dados para o resto do app.
3. **Integração de file picking** — `OpenFileDialog` com `multiple_select=True` e filtros; persistir paths na sessão; validação básica (extensão, tamanho). *Desbloqueia:* fluxo real de conteúdos no Android.
4. **Pipeline mínimo end-to-end** — um formato (ex. só imagem → PDF simples) com escrita em `app.paths.cache`; botão Ok chama pipeline via offload; mensagem de sucesso/erro. *Desbloqueia:* prova de arquitetura I/O + threading.
5. **Regras completas de marca d’água e endurecimento** — diagonal, multilinha, fonte embutida, não copiável, supressão OCR conforme desenho técnico. *Desbloqueia:* valor core; maior risco de dependências nativas — validar wheels Android cedo nesta fase.
6. **Export / download UX** — `SaveFileDialog`, nomes de arquivo sugeridos, tratamento de cancelamento; limpeza de temporários; fluxo **Sair**. *Desbloqueia:* entrega utilizável para compartilhamento com terceiros.

**Rationale de dependências:** diálogos e paths antes do pipeline pesado; pipeline “estreito” antes das regras visuais/PDF complexas; export por último para centralizar a UX em cima de arquivos já corretos.

## Sources

- Toga — [Dialogs reference](https://github.com/beeware/toga/blob/main/docs/en/reference/api/application/dialogs.md) (OpenFileDialog, SaveFileDialog, async `window.dialog`)
- Toga — [Paths API](https://github.com/beeware/toga/blob/main/docs/en/reference/api/data-representation/paths.md) (`app.paths.cache`, `data`, `config`, …)
- Toga — [File management topic](https://github.com/beeware/toga/blob/main/docs/en/topics/file-management.md) (`paths.app`, evitar CWD)
- Briefcase — [Gradle / Android](https://briefcase.readthedocs.io/en/stable/reference/platforms/android/gradle.html) (permissões, `requires`/wheels, quirks de pacotes de terceiros)
- Context7 — `/beeware/toga`, `/beeware/briefcase` (snippets alinhados às páginas acima)

---
*Architecture research for: BeeWare Android — UI, picking, pipeline, temp files, export*  
*Researched: 2026-05-12*
