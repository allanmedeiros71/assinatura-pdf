# Roadmap: MarcaJá

## Overview

Do projeto Briefcase/Toga funcional no Android até ao fluxo completo: escolher vários PDFs/imagens, definir texto de marca (com tipografia e geometria acordadas), processar em lote no dispositivo com progresso e erros claros, e obter PDFs endurecidos prontos a partilhar ou guardar — com gate cedo de dependências nativas (Chaquopy/PyMuPDF vs plano B) para evitar retrabalho, alinhado a PITFALLS e ARCHITECTURE da pesquisa.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [ ] **Phase 1: Fundação BeeWare e tela principal** — App Android em Python empacotado com BeeWare; uma tela Material; botões Ok/Sair; fonte open source incorporada e documentada.
- [ ] **Phase 2: Sessão, lista e texto da marca** — Seleção múltipla de ficheiros, lista editável e campo de marca com limite de 200 caracteres comunicado ao utilizador.
- [ ] **Phase 3: Motor PDF no Android, cache e saída PDF base** — Build Android com motor escolhido (ou facada + ramo provado); política de cache/limpeza; cada entrada válida gera um PDF de resultado (critério de pipeline antes do endurecimento total).
- [ ] **Phase 4: Marca diagonal, geometria e processamento em lote** — Marca alinhada à diagonal, tipografia proporcional, multilinha, texto refletido no output; processamento em série no dispositivo ao tocar Ok.
- [ ] **Phase 5: PDF endurecido, partilha e robustez de UI** — Texto não trivialmente copiável; sem OCR útil; partilhar/guardar; progresso por ficheiro; mensagens de erro legíveis.

## Phase Details

### Phase 1: Fundação BeeWare e tela principal
**Goal**: O utilizador abre uma app Android construída em Python com BeeWare e vê uma única tela principal com aspeto Android moderno, com ações Ok e Sair visíveis e a fonte de marca open source disponível para o projeto.
**Mode:** mvp
**Depends on**: Nothing (first phase)
**Requirements**: PLAT-01, UI-01, UI-02, UI-03, WM-07
**Success Criteria** (what must be TRUE):
  1. O utilizador instala e abre a app no Android (ou emulador alvo) gerada pelo fluxo Briefcase/Toga definido no repositório.
  2. Ao abrir, existe **uma única** tela principal sem onboarding obrigatório.
  3. A interface é reconhecível como Android moderno (Material / componentes Toga coerentes com Android no dispositivo).
  4. Os botões **Ok** e **Sair** estão visíveis na tela principal.
  5. A família tipográfica acordada (Arial ou equivalente open source, ex. Liberation Sans) está incorporada ou empacotada com menção de licença acessível ao projeto (README ou decisão documentada).
**Plans**: TBD
**UI hint**: yes

### Phase 2: Sessão, lista e texto da marca
**Goal**: O utilizador compõe o lote (vários PDFs/imagens), vê e corrige a lista antes de processar, e introduz o texto da marca com limite de 200 caracteres de forma previsível.
**Mode:** mvp
**Depends on**: Phase 1
**Requirements**: FILE-01, FILE-02, FILE-03, WM-01, WM-02
**Success Criteria** (what must be TRUE):
  1. O utilizador pode selecionar **múltiplos** ficheiros numa ação, incluindo PDF e imagens comuns (ex. PNG, JPEG).
  2. Antes de processar, a lista de ficheiros selecionados é **visível** com identificação suficiente para distinguir entradas.
  3. O utilizador pode **remover** uma entrada da lista sem sair do ecrã principal.
  4. Existe um campo de texto para o conteúdo da marca d'água.
  5. O campo aceita no máximo **200 caracteres**; entradas inválidas são bloqueadas ou truncadas de forma previsível e o utilizador vê feedback (ex.: contador ou mensagem curta).
**Plans**: TBD

### Phase 3: Motor PDF no Android, cache e saída PDF base
**Goal**: O pipeline corre no dispositivo com escrita em cache documentada e gera **PDF** como resultado por ficheiro válido, após validação empírica do motor no Android (incluindo plano B se necessário), sem depender de backend.
**Mode:** mvp
**Depends on**: Phase 2
**Requirements**: OUT-01, PROC-02, PROC-03
**Success Criteria** (what must be TRUE):
  1. `briefcase build android` (ou fluxo equivalente documentado) produz binário com o motor/facada acordados e registo da decisão PyMuPDF vs fallback (ex. PdfRenderer + Pillow + img2pdf) quando aplicável.
  2. Ficheiros temporários são escritos em diretórios de **cache** da aplicação segundo política documentada no repositório.
  3. Após sucesso ou abandono do fluxo, os temporários são **limpos** conforme essa política (comportamento verificável num cenário de teste descrito no plano).
  4. Todo o processamento demonstrado nesta fase ocorre **no dispositivo**, sem login nem chamadas a backend para o núcleo.
  5. Para cada entrada válida processada nesta fase, o utilizador obtém um ficheiro de saída em formato **PDF** (ainda que o endurecimento total seja afinado na Fase 5).
**Plans**: TBD

### Phase 4: Marca diagonal, geometria e processamento em lote
**Goal**: Ao tocar Ok, todos os ficheiros válidos da lista são processados em série com marca visual conforme geometria e tipografia acordadas, e o texto renderizado corresponde ao introduzido.
**Mode:** mvp
**Depends on**: Phase 3
**Requirements**: WM-03, WM-04, WM-05, WM-06, PROC-01
**Success Criteria** (what must be TRUE):
  1. Ao tocar **Ok**, todos os ficheiros **válidos** da lista são processados em **série** (sem ANR perceptível; estratégia documentada se usar threads/async).
  2. A marca renderizada corresponde ao **texto** introduzido (incluindo quebras de linha do utilizador, quando aplicável).
  3. A inclinação da marca está **alinhada** com a diagonal canto inferior esquerdo → canto superior direito da página (ou página rasterizada equivalente), verificável em PDF de referência de testes.
  4. O tamanho da fonte é **proporcional** de modo visualmente equilibrado ao longo dessa diagonal (critério de aceite com amostras no plano de testes).
  5. Se o texto for longo, o sistema **quebra em várias linhas** mantendo legibilidade mínima acordada (amostras no plano de testes).
**Plans**: TBD

### Phase 5: PDF endurecido, partilha e robustez de UI
**Goal**: Os PDFs gerados resistem a cópia trivial de texto e não incluem OCR útil; o utilizador obtém cada resultado via ações Android de partilha/guardar; durante o lote vê progresso e, em falha, mensagem legível por ficheiro.
**Mode:** mvp
**Depends on**: Phase 4
**Requirements**: OUT-02, OUT-03, OUT-04, UI-04, UI-05
**Success Criteria** (what must be TRUE):
  1. Nos PDFs gerados, o corpo do documento **não é seleccionável/copiável** de forma trivial (critério de aceite com teste manual/automatizado descrito no plano).
  2. Os PDFs gerados **não incluem camada OCR útil** para busca ou cópia do conteúdo original (critério alinhado a amostras de teste; linguagem honesta se houver limitações).
  3. O utilizador pode **obter** cada PDF gerado através de ação de sistema Android adequada (ex.: **Partilhar** e/ou **Guardar** / abrir noutra app), sem servidor próprio.
  4. Durante o processamento em lote, o utilizador vê **indicador de progresso** (ex.: ficheiro atual ou percentagem).
  5. Em falha de um ficheiro, o utilizador vê **mensagem de erro legível** que identifica o ficheiro ou a causa em termos humanos.
**Plans**: TBD
**UI hint**: yes

## Progress

**Execution Order:**

Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Fundação BeeWare e tela principal | 0/TBD | Not started | - |
| 2. Sessão, lista e texto da marca | 0/TBD | Not started | - |
| 3. Motor PDF no Android, cache e saída PDF base | 0/TBD | Not started | - |
| 4. Marca diagonal, geometria e processamento em lote | 0/TBD | Not started | - |
| 5. PDF endurecido, partilha e robustez de UI | 0/TBD | Not started | - |
