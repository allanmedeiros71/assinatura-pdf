# Feature Research

**Domain:** App Android local de marca d'água em texto sobre PDFs/imagens, saída PDF endurecida (uma tela, multi-arquivo).

**Researched:** 2026-05-12

**Confidence:** MEDIUM — paisagem derivada principalmente de `PROJECT.md` e padrões de mercado de apps de documento; benchmarks competitivos não foram medidos em laboratório.

## Feature Landscape

### Table Stakes (Users Expect These)

Recursos que usuários de apps de documento no Android assumem. Ausência gera frustração imediata.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Seleção de múltiplos arquivos (PDF e imagens) | Padrão de compartilhamento/galeria no Android | LOW–MEDIUM | Depende de intents SAF/photo picker e permissões de armazenamento (escopo limitado). |
| Campo de texto da marca (limite claro, ex. 200 caracteres) | Controle do que será impresso no documento | LOW | Validação + contador de caracteres. |
| Ação clara “processar” e saída acessível | Fluxo “escolher → confirmar → obter arquivo” | LOW | Botão Ok + feedback de progresso/erro. |
| Sair / encerrar fluxo sem surpresas | Evita sensação de app “preso” | LOW | Botão Sair; respeitar ciclo de vida Android. |
| Download ou compartilhamento dos PDFs gerados | Objetivo final é anexar a terceiros | MEDIUM | `ACTION_SEND` / salvar em Downloads; múltiplos arquivos pode exigir ZIP ou fila (decisão de produto). |
| Marca d'água visível e legível | Propósito do app | MEDIUM | Diagonal, fonte proporcional, quebra em linhas — já especificado no projeto. |
| Feedback durante processamento (lote) | PDFs grandes travam UI se síncrono | MEDIUM | Worker/thread + indicador; evita ANR no BeeWare/Toga. |
| Tratamento de erro legível (“falhou arquivo X”) | Confiança em uso com documentos sensíveis | LOW–MEDIUM | Depende de pipeline PDF/raster bem instrumentado. |

### Differentiators (Competitive Advantage)

O que alinha com **Core Value** do projeto: local, endurecido, pronto para terceiros (seguradoras, bancos).

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Processamento 100% no dispositivo (sem login/servidor) | Privacidade e narrativa simples de compliance informal | LOW (produto) / — | Stack já força isso; comunicar na UI reforça diferencial. |
| Saída sempre PDF com texto não copiável e OCR suprimido | Reduz extração trivial vs. marca só “visual” | HIGH | Núcleo técnico: rasterização, remoção de camada de texto/OCR, metadados; depende de biblioteca PDF + testes. |
| Marca diagonal com tipografia Arial/equivalente open source | Aparência “institucional” familiar | MEDIUM | Liberation Sans/Arimo; embedding ou raster consistente. |
| Fluxo de uma única tela | Velocidade mental para lote pequeno/médio | LOW–MEDIUM | Evita navegação; concentra complexidade na tela única (layout + estados). |
| Lote multi-arquivo em uma confirmação | Produtividade para pacotes de anexos | MEDIUM | Orquestração de fila, limites de memória no celular. |

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Contas, nuvem e sincronização | “Salvar meus presets” | Viola escopo sem backend; aumenta superfície legal e suporte | Manter 100% local; presets opcionais só em v2+ com armazenamento local explícito. |
| Marca d'água como texto PDF selecionável “para acessibilidade” | Pedidos de acessibilidade / cópia | Conflita com requisito de texto não copiável e supressão de OCR | Rasterizar marca; se necessário futuro, pesquisar caminho legal/UX separado (fora do escopo atual). |
| Editor WYSIWYG rico (cores, imagens, logos) | Personalização | Explode escopo e testes; BeeWare UI mais trabalhosa | Texto + parâmetros fixos conforme spec; adiar branding avançado. |
| OCR no output | “Buscar dentro do PDF” | Diretamente contra suprimir OCR | Não oferecer; documentar que o PDF é “cópia de exibição”. |
| Versões iOS/desktop no mesmo marco | Reuso de código | Fora do escopo do marco; dispersa validação | Manter Android até validar hipótese de valor. |
| Log/auditoria persistente de quem processou o quê | Compliance enterprise | Pedido típico mas fora do escopo; dados sensíveis | Sem logs persistentes; opcionalmente mensagens em memória só para debug em build dev. |

## Feature Dependencies

```
[Seleção multi-arquivo]
    └──requires──> [Pipeline de leitura PDF/imagem]
                       └──requires──> [Biblioteca PDF + decodificação de imagem]

[Marca d'água visível (diagonal, multilinha)]
    └──requires──> [Renderização (raster/graphics)]
                       └──requires──> [Fonte open source incorporada ou rasterizada]

[PDF endurecido — texto não copiável, sem OCR útil]
    └──requires──> [Rasterização ou remoção de texto/OCR da entrada]
                       └──requires──> [Geração PDF “só imagem” + flags/metadados coerentes]
                             └──requires──> [Pipeline estável e testado por amostra]

[Compartilhar/baixar resultados]
    └──requires──> [Arquivos temporários seguros + limpeza]
                       └──requires──> [Processamento em background / sem ANR]

[UI uma tela (Material)]
    └──enhances──> [Todos os fluxos acima] (estados: vazio, selecionado, processando, sucesso, erro)
```

### Dependency Notes

- **Seleção multi-arquivo → pipeline de leitura:** sem normalizar entradas (PDF vs imagem, orientação, DPI), marca e saída ficam inconsistentes.
- **Marca visível → renderização:** tamanho proporcional à diagonal depende de geometria da página rasterizada ou do box de texto; quebra em linhas depende de medição de texto.
- **PDF endurecido → raster/remoção de texto:** é o maior acoplamento técnico; decisões aqui impactam performance e tamanho do arquivo.
- **Compartilhar resultados → arquivos temporários:** lote grande exige política de limpeza e limite de disco; impacta UX de erro.
- **UI uma tela:** não é dependência dura de backend, mas concentra estados; falhas de layout afetam percepção de qualidade mais que em apps multi-tela.

## MVP Definition

### Launch With (v1)

Mínimo alinhado aos requisitos **Active** em `PROJECT.md`.

- [ ] Uma tela única (Material/moderno) com lista de arquivos selecionados, campo de marca (≤200), Ok e Sair.
- [ ] Seleção de múltiplos PDFs e/ou imagens.
- [ ] Processamento local em lote com feedback de progresso e cancelamento desejável (cancelamento: validar na fase de UX).
- [ ] Marca diagonal, multilinha, fonte Arial/equivalente open source.
- [ ] Saída PDF com política endurecida acordada (texto não copiável, OCR suprimido) — critérios de aceite testáveis com amostras reais.
- [ ] Entrega dos PDFs ao usuário (compartilhar e/ou salvar) de forma previsível.

### Add After Validation (v1.x)

- [ ] Limite explícito de tamanho/número de páginas por lote com mensagem clara — após medir performance em dispositivos alvo.
- [ ] Presets de texto de marca (armazenamento local) — se usuários pedirem repetibilidade.
- [ ] Pausa/retomada de lote ou fila persistente — se falhas de memória forem frequentes.

### Future Consideration (v2+)

- [ ] iOS/desktop (Briefcase multi-plataforma) — após validar Android.
- [ ] Marca com imagem/logo — novo pipeline gráfico e direitos de marca.
- [ ] Modo “apenas visual” (texto copiável) — só se houver requisito regulatório explícito; conflita com posicionamento atual.

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Seleção multi-arquivo + lista na tela | HIGH | MEDIUM | P1 |
| Campo de texto da marca + Ok/Sair | HIGH | LOW | P1 |
| Marca diagonal multilinha legível | HIGH | MEDIUM | P1 |
| PDF endurecido (não copiável, sem OCR útil) | HIGH | HIGH | P1 |
| Compartilhar/salvar PDFs gerados | HIGH | MEDIUM | P1 |
| Progresso/erros em lote | MEDIUM | MEDIUM | P1 |
| Cancelamento de processamento | MEDIUM | MEDIUM | P2 |
| Presets locais de texto | LOW | LOW | P3 |
| ZIP de múltiplos PDFs | MEDIUM | LOW–MEDIUM | P2 |

**Priority key:**

- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

## Competitor Feature Analysis

| Feature | Apps genéricos de escaneamento/marca | Suites PDF (Adobe etc.) | Our Approach |
|---------|--------------------------------------|-------------------------|--------------|
| Marca d'água em texto | Comum; muitas vezes só sobreposição visual | Recursos avançados (imagem, PDF real) | Texto + geometria fixa na spec; foco em simplicidade. |
| Privacidade / local | Variável; muitos oferecem nuvem opcional | Muitas contas e ecossistemas | 100% local como promessa central. |
| PDF “difícil de copiar” | Nem sempre prioridade; OCR frequente em scans | Controles de segurança enterprise | Diferencial explícito do projeto; exige prova com PDFs reais. |
| Uma tela, lote rápido | UX muitas vezes fragmentada | Poderoso porém pesado | Uma tela para reduzir atrito. |

*Nota:* nomes de concorrentes são ilustrativos; comparativo detalhado de apps exigiria pesquisa de mercado dedicada (LOW confidence para diferenças pontuais de recurso).

## Sources

- `/.planning/PROJECT.md` — requisitos ativos, fora de escopo, decisões (fonte primária, HIGH confidence para escopo).
- Template GSD `research-project/FEATURES.md` — estrutura do documento.
- Padrões gerais de apps Android de documento e leitores PDF (MEDIUM/LOW confidence; sem benchmark próprio nesta rodada).

---
*Feature research for: marca d'água local Android (PDF/imagem → PDF endurecido)*

*Researched: 2026-05-12*
