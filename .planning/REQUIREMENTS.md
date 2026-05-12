# Requirements: MarcaJá

**Defined:** 2026-05-12  
**Core Value:** Marcar vários PDFs/imagens de uma vez e obter PDFs endurecidos (texto não copiável, sem OCR útil) no smartphone, 100% local.  
**Milestone ativo:** **v1.0 — Execução MVP** (implementar e validar as fases **1 a 5** do `.planning/ROADMAP.md`; requisitos abaixo são o escopo deste marco).

## v1 Requirements

### Interface (uma tela)

- [ ] **UI-01**: Ao abrir o app, o usuário vê **uma única** tela principal (sem fluxo de onboarding obrigatório).
- [ ] **UI-02**: A interface segue padrões **Android modernos** (Material Design / componentes nativos BeeWare/Toga coerentes com Android).
- [ ] **UI-03**: A tela expõe explicitamente o botão **Ok** e o botão **Sair**.
- [ ] **UI-04**: Durante o processamento em lote, o usuário vê **indicador de progresso** (ex.: arquivo atual / porcentagem) para evitar bloqueio percebido.
- [ ] **UI-05**: Em falha de processamento de um arquivo, o usuário vê **mensagem de erro legível** identificando o arquivo ou a causa em termos humanos.

### Entrada de arquivos

- [ ] **FILE-01**: O usuário pode **selecionar múltiplos** arquivos numa ação (PDF e formatos de **imagem** comuns, ex. PNG/JPEG).
- [ ] **FILE-02**: A lista de arquivos selecionados é **visível** antes de processar (nome ou identificação suficiente para distinguir entradas).
- [ ] **FILE-03**: O usuário pode **remover** uma entrada da lista antes de processar (correção de erro simples sem abandonar a tela).

### Texto da marca

- [ ] **WM-01**: Existe um campo de texto para o conteúdo da marca d'água.
- [ ] **WM-02**: O campo aceita no máximo **200 caracteres**; entradas inválidas são bloqueadas ou truncadas de forma **previsível** e comunicada (ex.: contador).
- [ ] **WM-03**: A marca renderizada corresponde ao **texto** introduzido (incluindo quebras de linha introduzidas pelo usuário, se aplicável).

### Geometria e tipografia da marca

- [ ] **WM-04**: A inclinação da marca está **alinhada** com a diagonal que liga o canto **inferior esquerdo** ao **superior direito** da página (ou da página rasterizada equivalente).
- [ ] **WM-05**: O tamanho da fonte é **proporcional** de modo a ocupar de forma visualmente equilibrada a região ao longo dessa diagonal (critério observável em PDF de teste de referência).
- [ ] **WM-06**: Se o texto for longo, o sistema **quebra em várias linhas** de forma a manter legibilidade mínima acordada (critério de aceite com amostras no plano de testes).
- [ ] **WM-07**: Usa fonte da família **Arial** ou equivalente **open source** licenciada para incorporação (ex.: Liberation Sans, Arimo), documentada em `Key Decisions` ou README.

### Processamento e pipeline

- [ ] **PROC-01**: Ao tocar **Ok**, todos os arquivos válidos da lista são **processados em série** (ou de outra forma que evite ANR/memória excessiva documentada no plano).
- [ ] **PROC-02**: Todo o processamento ocorre **no dispositivo**; não é exigida conta, login nem chamadas a backend para a funcionalidade core.
- [ ] **PROC-03**: Arquivos temporários são escritos em diretórios de **cache** do aplicativo e **limpos** após sucesso ou abandono do fluxo (política documentada).

### Saída PDF endurecida

- [ ] **OUT-01**: Cada resultado é entregue como **PDF**, independentemente de a entrada ser PDF ou imagem.
- [ ] **OUT-02**: Nos PDFs gerados, o **texto do documento não é selecionável/copiável** de forma trivial (critério de aceite: teste manual/automatizado descrito no plano — ex.: ausência de camada de texto extractável para o corpo do documento).
- [ ] **OUT-03**: Os PDFs gerados **não incluem camada OCR útil** para busca ou cópia do conteúdo original (critério de aceite alinhado a amostras de teste; linguagem de produto honesta se houver limitações conhecidas).
- [ ] **OUT-04**: O usuário pode **obter** cada PDF gerado através de ação de sistema Android adequada (ex.: **Compartilhar** e/ou **Salvar** / abrir com outra app), sem depender de servidor próprio.

### Plataforma e entrega

- [ ] **PLAT-01**: O aplicativo é construído em **Python** e empacotada para **Android** com **BeeWare** (Briefcase/Toga), conforme decisão de projeto.

## v2 Requirements

### Entrega e robustez

- **ZIP-01**: Oferecer download único como **arquivo ZIP** com todos os PDFs do lote (opcional se OUT-04 cobrir bem o caso de uso).

### Operação

- **OPS-01**: Limite explícito de **tamanho/número de páginas** por lote com mensagem clara após medição em dispositivos alvo.

### Produto

- **PRE-01**: Presets de texto de marca guardados **localmente** (sem conta).

## Out of Scope

| Feature | Reason |
|---------|--------|
| Autenticação, contas, nuvem | Especificação explícita — app local sem login |
| Auditoria e logs persistentes | Fora do pedido; dados sensíveis |
| RBAC / perfis | Fora do pedido |
| iOS / desktop no mesmo marco | Foco Android até validar hipótese |
| OCR de busca no PDF de saída | Conflita com requisito de suprimir OCR |
| Editor WYSIWYG avançado (cores, logos) | Fora do MVP; aumenta escopo |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PLAT-01 | Phase 1 | Pending |
| UI-01 | Phase 1 | Pending |
| UI-02 | Phase 1 | Pending |
| UI-03 | Phase 1 | Pending |
| WM-07 | Phase 1 | Pending |
| FILE-01 | Phase 2 | Pending |
| FILE-02 | Phase 2 | Pending |
| FILE-03 | Phase 2 | Pending |
| WM-01 | Phase 2 | Pending |
| WM-02 | Phase 2 | Pending |
| OUT-01 | Phase 3 | Pending |
| PROC-02 | Phase 3 | Pending |
| PROC-03 | Phase 3 | Pending |
| WM-03 | Phase 4 | Pending |
| WM-04 | Phase 4 | Pending |
| WM-05 | Phase 4 | Pending |
| WM-06 | Phase 4 | Pending |
| PROC-01 | Phase 4 | Pending |
| OUT-02 | Phase 5 | Pending |
| OUT-03 | Phase 5 | Pending |
| OUT-04 | Phase 5 | Pending |
| UI-04 | Phase 5 | Pending |
| UI-05 | Phase 5 | Pending |

**Coverage:**

- v1 requirements: 23 total
- Mapped to phases: 23
- Unmapped: 0

---
*Requirements defined: 2026-05-12*  
*Last updated: 2026-05-12 after starting milestone v1.0 Execução MVP*
