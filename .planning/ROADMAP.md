# Roadmap: MarcaJá

## Overview

Do projeto Briefcase/Toga funcional no Android até o fluxo completo: escolher vários PDFs/imagens, definir texto de marca (com tipografia e geometria acordadas), processar em lote no dispositivo com progresso e erros claros, e obter PDFs endurecidos prontos para compartilhar ou salvar — com gate cedo de dependências nativas (Chaquopy/PyMuPDF vs plano B) para evitar retrabalho, alinhado a PITFALLS e ARCHITECTURE da pesquisa.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [ ] **Phase 1: Fundação BeeWare e tela principal** — App Android em Python empacotado com BeeWare; uma tela Material; botões Ok/Sair; fonte open source incorporada e documentada.
- [ ] **Phase 2: Sessão, lista e texto da marca** — Seleção múltipla de arquivos, lista editável e campo de marca com limite de 200 caracteres comunicado ao usuário.
- [ ] **Phase 3: Motor PDF no Android, cache e saída PDF base** — Build Android com motor escolhido (ou fachada + ramo provado); política de cache/limpeza; cada entrada válida gera um PDF de resultado (critério de pipeline antes do endurecimento total).
- [ ] **Phase 4: Marca diagonal, geometria e processamento em lote** — Marca alinhada à diagonal, tipografia proporcional, multilinha, texto refletido no output; processamento em série no dispositivo ao tocar Ok.
- [ ] **Phase 5: PDF endurecido, compartilhamento e robustez de UI** — Texto não trivialmente copiável; sem OCR útil; compartilhar/salvar; progresso por arquivo; mensagens de erro legíveis.

## Phase Details

### Phase 1: Fundação BeeWare e tela principal
**Goal**: O usuário abre uma app Android construída em Python com BeeWare e vê uma única tela principal com aspecto Android moderno, com ações Ok e Sair visíveis e a fonte de marca open source disponível para o projeto.
**Mode:** mvp
**Depends on**: Nothing (first phase)
**Requirements**: PLAT-01, UI-01, UI-02, UI-03, WM-07
**Success Criteria** (what must be TRUE):
  1. O usuário instala e abre a app no Android (ou emulador alvo) gerada pelo fluxo Briefcase/Toga definido no repositório.
  2. Ao abrir, existe **uma única** tela principal sem onboarding obrigatório.
  3. A interface é reconhecível como Android moderno (Material / componentes Toga coerentes com Android no dispositivo).
  4. Os botões **Ok** e **Sair** estão visíveis na tela principal.
  5. A família tipográfica acordada (Arial ou equivalente open source, ex. Liberation Sans) está incorporada ou empacotada com menção de licença acessível ao projeto (README ou decisão documentada).
**Plans**: TBD
**UI hint**: yes

### Phase 2: Sessão, lista e texto da marca
**Goal**: O usuário compõe o lote (vários PDFs/imagens), vê e corrige a lista antes de processar, e introduz o texto da marca com limite de 200 caracteres de forma previsível.
**Mode:** mvp
**Depends on**: Phase 1
**Requirements**: FILE-01, FILE-02, FILE-03, WM-01, WM-02
**Success Criteria** (what must be TRUE):
  1. O usuário pode selecionar **múltiplos** arquivos numa ação, incluindo PDF e imagens comuns (ex. PNG, JPEG).
  2. Antes de processar, a lista de arquivos selecionados é **visível** com identificação suficiente para distinguir entradas.
  3. O usuário pode **remover** uma entrada da lista sem sair da tela principal.
  4. Existe um campo de texto para o conteúdo da marca d'água.
  5. O campo aceita no máximo **200 caracteres**; entradas inválidas são bloqueadas ou truncadas de forma previsível e o usuário vê feedback (ex.: contador ou mensagem curta).
**Plans**: TBD

### Phase 3: Motor PDF no Android, cache e saída PDF base
**Goal**: O pipeline corre no dispositivo com escrita em cache documentada e gera **PDF** como resultado por arquivo válido, após validação empírica do motor no Android (incluindo plano B se necessário), sem depender de backend.
**Mode:** mvp
**Depends on**: Phase 2
**Requirements**: OUT-01, PROC-02, PROC-03
**Success Criteria** (what must be TRUE):
  1. `briefcase build android` (ou fluxo equivalente documentado) produz binário com o motor/fachada acordados e registro da decisão PyMuPDF vs fallback (ex. PdfRenderer + Pillow + img2pdf) quando aplicável.
  2. Arquivos temporários são escritos em diretórios de **cache** do aplicativo segundo política documentada no repositório.
  3. Após sucesso ou abandono do fluxo, os temporários são **limpos** conforme essa política (comportamento verificável num cenário de teste descrito no plano).
  4. Todo o processamento demonstrado nesta fase ocorre **no dispositivo**, sem login nem chamadas a backend para o núcleo.
  5. Para cada entrada válida processada nesta fase, o usuário obtém um arquivo de saída em formato **PDF** (ainda que o endurecimento total seja afinado na Fase 5).
**Plans**: TBD

### Phase 4: Marca diagonal, geometria e processamento em lote
**Goal**: Ao tocar Ok, todos os arquivos válidos da lista são processados em série com marca visual conforme geometria e tipografia acordadas, e o texto renderizado corresponde ao introduzido.
**Mode:** mvp
**Depends on**: Phase 3
**Requirements**: WM-03, WM-04, WM-05, WM-06, PROC-01
**Success Criteria** (what must be TRUE):
  1. Ao tocar **Ok**, todos os arquivos **válidos** da lista são processados em **série** (sem ANR perceptível; estratégia documentada se usar threads/async).
  2. A marca renderizada corresponde ao **texto** introduzido (incluindo quebras de linha do usuário, quando aplicável).
  3. A inclinação da marca está **alinhada** com a diagonal canto inferior esquerdo → canto superior direito da página (ou página rasterizada equivalente), verificável em PDF de referência de testes.
  4. O tamanho da fonte é **proporcional** de modo visualmente equilibrado ao longo dessa diagonal (critério de aceite com amostras no plano de testes).
  5. Se o texto for longo, o sistema **quebra em várias linhas** mantendo legibilidade mínima acordada (amostras no plano de testes).
**Plans**: TBD

### Phase 5: PDF endurecido, compartilhamento e robustez de UI
**Goal**: Os PDFs gerados resistem a cópia trivial de texto e não incluem OCR útil; o usuário obtém cada resultado via ações Android de compartilhar/salvar; durante o lote vê progresso e, em falha, mensagem legível por arquivo.
**Mode:** mvp
**Depends on**: Phase 4
**Requirements**: OUT-02, OUT-03, OUT-04, UI-04, UI-05
**Success Criteria** (what must be TRUE):
  1. Nos PDFs gerados, o corpo do documento **não é selecionável/copiável** de forma trivial (critério de aceite com teste manual/automatizado descrito no plano).
  2. Os PDFs gerados **não incluem camada OCR útil** para busca ou cópia do conteúdo original (critério alinhado a amostras de teste; linguagem honesta se houver limitações).
  3. O usuário pode **obter** cada PDF gerado através de ação de sistema Android adequada (ex.: **Compartilhar** e/ou **Salvar** / abrir em outra app), sem servidor próprio.
  4. Durante o processamento em lote, o usuário vê **indicador de progresso** (ex.: arquivo atual ou porcentagem).
  5. Em falha de um arquivo, o usuário vê **mensagem de erro legível** que identifica o arquivo ou a causa em termos humanos.
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
| 5. PDF endurecido, compartilhamento e robustez de UI | 0/TBD | Not started | - |
