# Project Research Summary

**Project:** MarcaJá (Android, app local de marca d'água em PDF/imagem)
**Domain:** App Android nativo em Python (BeeWare: Briefcase + Toga) — marca d'água em lote sobre PDFs/imagens, saída em PDF “endurecido” (texto não copiável, sem OCR útil), 100% no dispositivo
**Researched:** 2026-05-12
**Confidence:** MEDIUM

## Executive Summary

O produto é um **cliente Android local** orientado a fluxo único: seleção múltipla de arquivos, texto de marca (≤200 caracteres), processamento em lote e entrega de PDFs prontos para compartilhamento com terceiros. A documentação BeeWare indica construir com **Briefcase 0.4.x**, **Toga 0.5.x**, **Python 3.12** (mínimo 3.10), pipeline Python isolado da UI, **I/O via `app.paths.cache`** e **handlers assíncronos** com trabalho CPU-bound movido para thread (`asyncio.to_thread`), evitando ANR e violações de thread na UI nativa.

A abordagem recomendada é **PyMuPDF como motor principal** em desktop e *se* empacotar no Android; caso o wheel **não** esteja disponível no ecossistema Chaquopy (risco documentado — PyMuPDF não figura no índice público de pacotes nativos), ativar **plano B desde o primeiro sprint**: `PdfRenderer` (JNI via **rubicon-java**) + **Pillow** + **img2pdf** + **pypdf** para permissões/metadados. Manter a **mesma lógica de marca em Pillow** nos dois ramos reduz divergência visual. Complementar com **pypdf 6.x**, **Pillow**, **img2pdf** e fonte **OFL** (ex. Liberation Sans) empacotada com arquivos de licença.

Os riscos dominantes são: **(1)** expectativas irreais de “segurança absoluta” (PDF é orientação ao leitor; OCR externo e captura de tela contornam); mitigar com **copy honesto**, testes de extração e pipeline de **reconstrução de página** sem texto invisível. **(2)** **URIs SAF vs paths** e falhas só vistas no dispositivo — mitigar com spike Android cedo, cópia para cache e matriz de origens (Drive, Downloads, galeria). **(3)** **OOM** em rasterização — fila sequencial, limites de DPI/páginas, liberação explícita de documentos/pixmaps. **(4)** **Dependências nativas** — gate de build `briefcase build android` antes de fechar arquitetura.

## Key Findings

### Recommended Stack

Resumo em [STACK.md](./STACK.md): stack BeeWare oficial com pins explícitos; o ponto frágil é **PyMuPDF no Android**, que exige **validação empírica** ou fallback híbrido Java/Python.

**Core technologies:**
- **Python 3.12.x** — linguagem única; alinha `requires_python` Briefcase/Toga e Chaquopy; igualar major.minor no build e no target.
- **Briefcase 0.4.2** — APK/AAB, Gradle, Java 17, SDK; empacotamento Android canónico BeeWare.
- **Toga 0.5.4** — UI nativa Android, diálogos de arquivo, integração com ciclo de vida da app.
- **PyMuPDF ~1.27** — abrir PDF, rasterizar, marca, saída imagem-only e permissões *se* disponível no dispositivo de build.
- **pypdf 6.x + Pillow + img2pdf + rubicon-java 0.2.6** — camada complementar, montagem só-imagem, e ponte para **PdfRenderer** no plano B.

### Expected Features

Resumo em [FEATURES.md](./FEATURES.md); confiança **MEDIUM** (derivado de PROJECT.md + padrões de mercado).

**Must have (table stakes):**
- Seleção múltipla PDF/imagem e lista na tela — expectativa Android; SAF/intents.
- Campo de marca (≤200), Ok/Sair, fluxo claro — controlo e saída do fluxo.
- Processamento local em lote com progresso e erros por arquivo — evita ANR e abandono.
- Marca diagonal multilinha legível (fonte open source) — requisito visual do PROJECT.
- PDF endurecido (texto não copiável, OCR suprimido) — núcleo de valor; critérios de aceite testáveis.
- Compartilhar/salvar resultados — objetivo final do usuário.

**Should have (competitive):**
- 100% local sem login — narrativa de privacidade e compliance informal.
- Uma única tela — redução de atrito vs. suites pesadas.
- ZIP de múltiplos PDFs ou estratégia de lote (P2) — produtividade em anexos.

**Defer (v2+):**
- Contas/nuvem, editor WYSIWYG rico, marca como texto selecionável, iOS/desktop, OCR no output, auditoria persistente.

### Architecture Approach

Resumo em [ARCHITECTURE.md](./ARCHITECTURE.md): separação **Toga (apresentação + orquestração async)** / **session (estado)** / **pipeline (Python puro)** / **temporários em `app.paths.cache`**; sem widgets no worker; progresso incremental no lote.

**Major components:**
1. **MainWindow + `ui/`** — layout de tela única, binding e refresco após operações.
2. **Session / estado** — lista de arquivos, texto da marca, erros por item; fonte de verdade para a UI.
3. **Dialog coordinator** — `OpenFileDialog` (`multiple_select=True`) e `SaveFileDialog`; fluxos `async`.
4. **Pipeline** (`validate`, `watermark`, `harden_pdf`) — `process(in, texto) -> out_path` testável sem emulador.
5. **Packaging Briefcase** — permissões, Gradle, recursos (fontes).

### Critical Pitfalls

Top issues de [PITFALLS.md](./PITFALLS.md) com mitigação:

1. **“Segurança forte” só com flags PDF** — permissões não são criptografia; rasterização incompleta deixa texto/OCR/anexos. *Evitar:* mensagem de produto conservadora + pipeline que remove conteúdo textual e valida extração.
2. **“Remover OCR” superficial** — texto invisível ou dupla camada permanece recuperável. *Evitar:* reconstrução de página sem operadores de texto relevantes + inspeção estrutural do output.
3. **Paths de desktop no Android / SAF** — URIs revogáveis vs `open(path)`; falhas intermitentes. *Evitar:* cópia para cache, testes em hardware, camada de I/O que abstrai URI vs arquivo.
4. **OOM em raster + lote** — pixmaps grandes × páginas × paralelismo. *Evitar:* processamento sequencial, caps de DPI/dimensão, `close()` explícito, limites documentados.
5. **Wheels nativos inexistentes no Chaquopy** — dias perdidos “funciona no laptop”. *Evitar:* spike de dependências com critério de saída antes do desenvolvimento completo do pipeline.

## Implications for Roadmap

Com base na pesquisa conjunta (STACK + FEATURES + ARCHITECTURE + PITFALLS), fases sugeridas para o roadmapper:

### Phase 1: Fundação BeeWare e conformidade base
**Rationale:** Desbloqueia iteração real em dispositivo e antecipa bloqueios legais de fontes e template Android.
**Delivers:** Projeto Briefcase/Toga, janela única esquelética, tema Material, recursos de fonte OFL + LICENSE/COPYRIGHT, nota “Sobre” ou assets legais mínimos.
**Addresses:** Requisito BeeWare/Android; fonte equivalente a Arial (STACK, PITFALLS 5).
**Avoids:** Uso de Arial proprietária sem licença; CWD como pasta de trabalho (ARCHITECTURE anti-patterns).

### Phase 2: Sessão, lista e picking multi-arquivo
**Rationale:** O fluxo de dados (URIs, cópia, lista) é pré-requisito de qualquer PDF; falhas aqui são o Pitfall 3.
**Delivers:** `session.py`, UI de lista, `OpenFileDialog` com filtros, validação básica (extensão, tamanho), normalização para processamento estável.
**Addresses:** P1 seleção multi-arquivo + lista (FEATURES).
**Avoids:** Assumir paths POSIX estáveis em Android; testar só no `briefcase dev` desktop.

### Phase 3: Spike / gate de dependências PDF no Android
**Rationale:** Decisão arquitetural bloqueante (STACK MEDIUM, PITFALLS 6); deve preceder investimento pesado em endurecimento.
**Delivers:** `briefcase build android` com matriz de dependências; documento de decisão: ramo PyMuPDF vs PdfRenderer+Pillow+img2pdf; interface mínima do motor atrás de uma fachada.
**Addresses:** Risco técnico do valor core (PDF endurecido).
**Avoids:** Fixar PyMuPDF sem prova de wheel; paralelizar processamento nativo pesado no primeiro corte.

### Phase 4: Pipeline endurecido + marca diagonal
**Rationale:** Maior custo e acoplamento (FEATURES); depende do motor escolhido na Fase 3 e dos patterns de offload (ARCHITECTURE).
**Delivers:** `watermark.py` + `harden_pdf.py`, testes com amostras reais, critérios “zero texto extraível” / inspeção OCR; política de metadados e anexos.
**Addresses:** P1 marca diagonal multilinha + PDF endurecido (FEATURES).
**Avoids:** Pitfalls 1–2 (falsa segurança, OCR fantasma); processar na thread da UI.

### Phase 5: Export, compartilhamento e robustez de lote
**Rationale:** Entrega utilizável e limpeza de temporários fecham o loop com terceiros; depende de PDFs corretos em cache.
**Delivers:** `SaveFileDialog`, nomes sugeridos, compartilhamento/salvamento, limpeza de `app.paths.cache`, mensagens de erro específicas, progresso/cancelamento (cancelamento P2 conforme UX).
**Addresses:** P1 compartilhar/salvar + progresso/erros (FEATURES).
**Avoids:** Acumulação de temporários (PITFALLS performance); export opaco ao usuário.

### Phase 6: Polimento Play Store / empacotamento (se no âmbito do marco)
**Rationale:** Briefcase exige artefatos assinados; políticas de dados podem exigir clarificação mesmo sem backend.
**Delivers:** `briefcase package` assinado, `version_code`, checklist privacidade/rede conforme template actual.
**Addresses:** Distribuição real vs. sideload (PITFALLS secção Play Store).
**Avoids:** Distribuir binários não assinados como “prontos”.

### Phase Ordering Rationale

- **Diálogos, paths e spike nativo antes do endurecimento completo** — reduz retrabalho e valida o maior risco (Chaquopy + PDF).
- **Pipeline puro separado da UI** — habilita testes e troca de motor (PyMuPDF ↔ JNI) com custo controlado.
- **Copy de segurança e testes de extração em paralelo ao “PDF duro”** — alinha expectativas de stakeholders com a realidade do formato.

### Research Flags

Fases que provavelmente precisam de **`/gsd-research-phase`** ou spike dedicado durante o planeamento:

- **Fase 3 (gate PDF Android):** integração Chaquopy/wheels, possível JNI `PdfRenderer`, matriz de ABI — documentação esparsa para casos extremos.
- **Fase 4 (endurecimento):** semântica exacta de “sem OCR útil” por tipo de entrada; pode exigir pesquisa adicional por amostra de domínio (seguros/bancos).
- **Fase 5 (export Android):** FileProvider, intents de compartilhamento, comportamento exato de `SaveFileDialog` no backend Android — validar em dispositivo físico.

Fases com padrões mais estáveis (pesquisa fase opcional):

- **Fase 1 (scaffold BeeWare):** documentação oficial Briefcase/Toga para Android e Gradle.
- **Fase 2 (sessão + lista):** padrões Toga async + estado em memória bem documentados.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | MEDIUM–HIGH | Forte para BeeWare/Toga/Briefcase (PyPI + docs); **MEDIUM** no motor PDF Android por incerteza Chaquopy/PyMuPDF. |
| Features | MEDIUM | Primário alinhado a PROJECT.md; landscape competitivo sem benchmarks próprios. |
| Architecture | MEDIUM | Padrões oficiais Toga/Briefcase sólidos; paridade Material e quirks de diálogos Android requerem validação em dispositivo. |
| Pitfalls | MEDIUM | Mix de docs oficiais, issues de bibliotecas e material educativo de PDF; vários pontos dependem de testes no alvo. |

**Overall confidence:** MEDIUM

### Gaps to Address

- **Disponibilidade real de PyMuPDF no build Android do projecto:** confirmar com `briefcase build android` limpo; definir fallback operacional antes do roadmap fechar custos.
- **Comportamento exato de picking/salvar por versão Toga:** validar `OpenFileDialog`/`SaveFileDialog` em Android físico (ARCHITECTURE nota).
- **Definição mensurável de “OCR suprimido”** por classe de PDF de entrada: pode precisar de conjunto de testes representativo do domínio.
- **Política Play Store / permissão INTERNET** no template Briefcase: rever implicações de privacidade declarada mesmo para app offline.

## Sources

### Primary (HIGH confidence)

- [Briefcase — Gradle / Android](https://briefcase.readthedocs.io/en/stable/reference/platforms/android/gradle.html) — permissões, empacotamento, assinatura
- [BeeWare docs hub](https://docs.beeware.org/) — contexto geral do ecossistema
- [Toga — dialogs](https://github.com/beeware/toga/blob/main/docs/en/reference/api/application/dialogs.md) — `OpenFileDialog`, `SaveFileDialog`, async
- [Toga — Paths](https://github.com/beeware/toga/blob/main/docs/en/reference/api/data-representation/paths.md) — `app.paths.cache`, gestão de arquivos
- [Chaquopy — Android](https://chaquo.com/chaquopy/doc/current/android.html) — plugin Gradle, Python, `buildPython`, ABIs
- [Chaquopy PyPI index](https://chaquo.com/pypi-13.1/) — verificação de pacotes nativos (ausência de `pymupdf` listado)
- [Liberation Fonts LICENSE (SIL OFL)](https://github.com/liberationfonts/liberation-fonts/blob/main/LICENSE) — licenciamento de fontes
- **PyPI JSON** — versões pins: briefcase, toga, pymupdf, pypdf, Pillow, etc.
- **`/.planning/PROJECT.md`** — requisitos ativos e fora de escopo (fonte de produto)

### Secondary (MEDIUM confidence)

- **Context7** — `/beeware/briefcase`, `/beeware/toga` — snippets alinhados à documentação
- Issues/community **Chaquopy**, **PyMuPDF**, **pypdf** — riscos de memória e wheels Android
- [Toga — file management topic](https://github.com/beeware/toga/blob/main/docs/en/topics/file-management.md) — anti-patterns CWD
- Material educativo PDF (flatten vs rasterize, camadas ocultas) — modelo mental, não norma legal

### Tertiary (LOW confidence)

- Relatos de blog/third-party sobre paths Android `briefcase run` — sintomas úteis, não substituem reprodução local

---
*Research completed: 2026-05-12*
*Ready for roadmap: yes*
