# Pitfalls Research

**Domain:** App Android local (Python/BeeWare) — marca d’água em PDF, texto não copiável e supressão de camadas OCR  
**Researched:** 2026-05-12  
**Confidence:** MEDIUM (mistura de documentação oficial BeeWare/Android, issues de bibliotecas PDF e material de segurança de PDF; alguns pontos exigem validação no dispositivo alvo)

## Critical Pitfalls

### Pitfall 1: Prometer “segurança forte” com truques de PDF em vez de modelo de dados

**What goes wrong:**  
Stakeholders ou utilizadores assumem que “PDF com restrições + sem texto selecionável” impede extração ou reutilização do conteúdo. Na prática, **permissões de PDF e flags de cópia são orientação ao leitor**, não criptografia; rasterização mal feita pode deixar **streams de texto, anotações, metadados ou camadas OCR**; mesmo com página só em imagem, **OCR pode ser voltado a aplicar** ao resultado (novo texto “recuperável”). Screenshots e fotografias do ecrã contornam qualquer solução puramente de ficheiro.

**Why it happens:**  
Confundir **experiência de utilizador** (não consigo copiar no Acrobat) com **garantia de confidencialidade**. PDF é um contentor de objetos com múltiplas representações (aparência vs. texto vs. invisible text).

**How to avoid:**  
Definir **mensagem de produto honesta**: ex. “dificulta cópia de texto e reutilização casual”, não “impossível extrair”. Tecnicamente: pipeline que **elimina ou substitui todo o conteúdo vetorial/texto**, remove **Tagged PDF / estruturas acessíveis** quando aplicável, **anexos e comentários**, e valida o output com extração de texto + inspeção de camadas. Documentar limitações (OCR de terceiros, fotografia do ecrã).

**Warning signs:**  
Ainda consegue-se copiar texto no visualizador; `strings` ou ferramentas de extração mostram texto; ficheiro desce de tamanho mas mantém estrutura rica; testes só em “pré-visualização” do próprio app.

**Phase to address:**  
Fase de **contrato de segurança do PDF + validação** (antes de UX final).

---

### Pitfall 2: “Remover OCR” como marketing em vez de operação precisa

**What goes wrong:**  
O requisito “sem camada OCR útil” é interpretado como apagar um botão; ficam **Invisible text** alinhado à imagem, **dupla camada** (bitmap + texto), ou **metadados de reconhecimento** que ferramentas reconstituem. Em PDFs digitalizados com OCR prévio, **remover só a imagem visível** deixa o texto oculto recuperável.

**Why it happens:**  
OCR é frequentemente uma **subcamada de texto** independente da imagem; ferramentas de “marca d’água” desenham por cima sem destruir o stream subjacente.

**How to avoid:**  
Tratar “remover OCR” como **reconstrução da página**: rasterizar (ou reflow) e **garantir ausência de operadores de texto** e de **dicionários de OCR** associados; revalidar com leitores e bibliotecas de extração. Se a entrada já for só imagem, decidir explicitamente se o output **re-OCR** é aceitável para o caso de uso (geralmente não, se o objetivo é minimizar texto máquina-legível).

**Warning signs:**  
Pesquisa no PDF ainda encontra palavras da página original; tamanho do ficheiro sugere streams duplicados; acessibilidade ainda anuncia texto.

**Phase to address:**  
**Pipeline PDF** (mesma fase que geração da saída “endurecida”).

---

### Pitfall 3: Tratar caminhos de ficheiro no Android como no `briefcase dev`

**What goes wrong:**  
Código que usa `open()` com **path POSIX** ou diretórios “ao lado do script” funciona no desktop e **falha no dispositivo** (`FileNotFoundError`, pastas sob `files/` ou Chaquopy que não existem no momento esperado). Com **Storage Access Framework (SAF)**, o utilizador devolve **content URI**, não path estável — leitura/escrita exige **ContentResolver**, streams temporários e, muitas vezes, **cópia para cache interno** antes de bibliotecas PDF que só aceitam `path`.

**Why it happens:**  
Diferença entre **filesystem do pacote**, **scoped storage** e **URIs revogáveis**; exemplos e tutoriais BeeWare/desktop não stressam I/O real em Android.

**How to avoid:**  
Testar cedo em **hardware/emulador**; encapsular “obter bytes do input” e “entregar output” numa camada que suporte **URI + ficheiro temporário**; confirmar versão de **Toga**/`open_file_dialog` e documentação atual (Android usa **Intents** / `start_activity` onde necessário — ver referência oficial Toga Android).

**Warning signs:**  
Só testado com ficheiros em `~/Downloads` no Mac; exceções só no primeiro run Android; permissões declaradas mas URI nunca persistido.

**Phase to address:**  
**Integração Android + seleção de ficheiros** (fase inicial, em paralelo com spike de PDF).

---

### Pitfall 4: Subestimar RAM e pico de memória em lotes de PDFs grandes

**What goes wrong:**  
**Rasterização página a página** com pixmaps de alta resolução, ou PDFs com **content streams enormes**, pode causar **OOM** ou matar o processo Chaquopy. Bibliotecas como **PyMuPDF** podem reter memória após `get_pixmap()` se o ciclo de vida de `Document`/`Pixmap` não for gerido; **pypdf** tem relatos de uso extremo de RAM em páginas “pesadas”.

**Why it happens:**  
Desktop tem margem; telemóvel não. Processar **vários ficheiros em paralelo** ou manter **todos os bytes** em memória multiplica o pico.

**How to avoid:**  
Pipeline **sequencial** por ficheiro e por página; limites explícitos (DPI máximo, dimensão máxima da página, recusa ou downscale de entradas anómalas); **`close()`** / libertação explícita; testes com PDFs grandes reais; considerar escrita em disco temporário em chunks quando a API permitir.

**Warning signs:**  
App reinicia ao processar certos anexos; crescimento monotónico de memória em lote; ANRs durante escrita do PDF.

**Phase to address:**  
**Pipeline PDF + performance** (antes de otimização fina de UX).

---

### Pitfall 5: Usar Arial embutido sem licença (e ignorar obrigações de fontes open source)

**What goes wrong:**  
**Arial** é propriedade da Monotype; embutir ou redistribuir sem licença adequada expõe a **risco legal** e rejeição em lojas. Mesmo com **Liberation Sans / Arimo** (alternativas comuns), licenças tipo **SIL OFL** exigem **créditos e ficheiros de licença** no pacote da app e boas práticas de **Reserved Font Names** se houver subsetting com renomeação incorreta.

**Why it happens:**  
“Arial ou equivalente” na especificação é lido como “usar Arial do sistema”; no Android + bundle BeeWare o que conta é **o que vai no APK** e o que o motor PDF embute.

**How to avoid:**  
Escolher uma família **OFL** (ex. Liberation Sans), **incluir LICENSE + COPYRIGHT** na app (ecrã Sobre / assets legais), e validar subsetting/embedding conforme a licença da fonte escolhida.

**Warning signs:**  
Nenhum ficheiro de licença de fontes no repositório; PDF gerado referencia fontes não empacotadas de forma ambígua.

**Phase to address:**  
**Fundação do projeto + conformidade** (início).

---

### Pitfall 6: Assumir que qualquer biblioteca PDF do PyPI funciona no Android (Chaquopy)

**What goes wrong:**  
Dependência com **extensão nativa** sem wheel **android_*** disponível no índice Chaquopy/PyPI → build falha ou runtime quebrado. Equipa perde dias a “funciona no laptop”.

**Why it happens:**  
Documentação Briefcase deixa explícito que **a maioria dos projetos não publica wheels Android**; BeeWare depende de repositório secundário com cobertura incompleta.

**How to avoid:**  
Validar **cada dependência** (`requires`) contra a matriz Chaquopy **antes** de fixar arquitetura; preferir **pure Python** onde possível ou bibliotecas com wheels Android conhecidos; ter plano B (versão alternativa, fork, ou processamento híbrido).

**Warning signs:**  
Mensagens do tipo “No matching distributions” ou “Could not find a version” no `briefcase build android`.

**Phase to address:**  
**Spike técnico / arquitetura** (gate antes de implementação completa).

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Confiar só em **flags de permissão PDF** (sem rasterizar) | Implementação rápida | Utilizador avançado ou ferramenta ignora restrições; falsa sensação de segurança | **Nunca** para o valor prometido no PROJECT.md |
| Rasterizar mas **não limpar metadados/XMP** | Menos código | Fuga de dados contextuais (autor, título, software) | MVP interno apenas; documentar |
| **Bufferizar PDF inteiro** em `bytes` para cada item do lote | Código simples | OOM em lotes médios | Apenas ficheiros pequenos com limite rígido documentado |
| Dependência PDF “pesada” sem prova em **arm64** | Features ricas | Bloqueio de release Android | Só durante spike com **critério de saída** |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| **SAF / content URI** | Passar URI como se fosse path POSIX | Abrir via APIs Android (`ContentResolver.openInputStream`), copiar para temp se necessário |
| **Partilha / download do resultado** | Escrever só para diretório interno opaco ao utilizador | Usar **FileProvider** / intent de partilha com URI com permissão temporária, conforme padrão Android |
| **Toga Android** | Ignorar `start_activity` e callbacks de resultado | Seguir documentação oficial para Intents quando o fluxo cruzar fronteira Java/Python |
| **Briefcase `permission.*`** | Pedir `READ_MEDIA_*` sem necessidade | Pedir apenas permissões mapeadas ao caso (ex. galeria); rever doc Briefcase para efeitos colaterais em `features` |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Pixmap alta resolução × N páginas | OOM, app a fechar | DPI cap, processar e libertar página a página | PDFs de muitas páginas ou páginas A3 digitalizadas |
| PDF com streams gigantes (vector art) | Congelamento, RAM em GB no desktop | Timeout/recusa, simplificar pipeline ou biblioteca | Anexos “impressos” de CAD ou slides complexos |
| Lote **multi-ficheiro** em paralelo | Pico de RAM | Fila sequencial + limite explícito de ficheiros por operação | Utilizador seleciona dezenas de MB de uma vez |
| Acumulação de temporários | Armazenamento cheio | Limpar `cache`/`files` após partilha bem-sucedida | Uso repetido no mesmo dia |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Vender **“sem cópia”** como **irreversível** | Fraude de expectativa, responsabilidade | Linguagem conservadora + testes de extração documentados |
| Rasterizar por cima mantendo **texto invisível** | Recuperação trivial de texto | Pipeline de reconstrução + testes automatizados de “zero texto extraível” |
| Manter **anotações / attachments** do PDF original | Dados sensíveis fora da área visível | Strip ou novo PDF mínimo |
| Ficheiros temporários com nomes previsíveis em diretório legível | Leak para outras apps (consoante API level e permissões) | Diretório privado da app + apagar após uso |
| Logs de debug com **caminhos ou excertos** de documentos | Privacidade | Sem logs persistentes (alinhado ao out of scope, mas cuidado em builds de debug) |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Processamento longo **sem progresso** | Utilizador assume crash e força fecho | Barra ou por página + cancelamento |
| Falha genérica “Erro ao processar” | Abandono | Mensagens por causa (ficheiro demasiado grande, formato, memória) sem expor dados |
| Output não abre na app de email do banco | “O app não funciona” | Testar com leitores comuns + tamanho de ficheiro |
| Marca d’água ilegível em ecrãs pequenos | Reclamações | Pré-visualização ou ajuste dinâmico da diagonal/fonte |

## "Looks Done But Isn't" Checklist

- [ ] **Texto não copiável:** Verificar em pelo menos dois leitores (ex. Google PDF, Adobe) + tentativa de extração programática — não só desativar seleção na UI interna.
- [ ] **OCR / camadas:** Abrir output em ferramenta que mostre estrutura de conteúdo; procurar texto invisível ou dicionários típicos de OCR.
- [ ] **Android file path:** Testar pick de ficheiro da Drive, Downloads e galeria — não só ficheiro local “simples”.
- [ ] **Lote:** Processar N>5 ficheiros médios sem reinício de processo.
- [ ] **Fontes:** Presença de ficheiros de licença e embedding conforme OFL.
- [ ] **Assinatura / empacotamento:** Artefacto `briefcase package` **assinado** antes de distribuição (Play ou sideload) — o template Briefcase indica que **não é utilizável sem assinatura**.

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Biblioteca PDF incompatível com Android | HIGH | Trocar biblioteca ou reduzir funcionalidade; spike paralelo |
| OOM em produção | MEDIUM | Limites de entrada + mensagem; reduzir DPI; fila |
| Expectativa de segurança incorreta | Médio (reputação) | Corrigir copy de produto; FAQ técnico |
| URI inválido após rotação | LOW | Re-picker; persistir permissão persistível se usar SAF adequado |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Expectativa segurança vs rasterização | Definição de pipeline + copy de produto | Extração de texto + checklist “Looks done” |
| OCR / camadas ocultas | Geração PDF endurecida | Inspeção estrutural + OCR de terceiros no output |
| Ficheiros Android / URI | Integração entrada/saída | Matriz de origens (Drive, Downloads, fotos) |
| Memória / lotes | Pipeline + limites | Testes com PDFs grandes e lote |
| Licença de fontes | Conformidade inicial | Auditoria de assets legais |
| Wheels Chaquopy | Spike dependências | CI ou build Android limpo |

## Sources

- [Briefcase — Gradle Android (permissões, quirks de pacotes terceiros, assinatura)](https://briefcase.beeware.org/en/stable/reference/platforms/android/gradle.html) — **HIGH** para BeeWare/Android packaging  
- [Toga — plataforma Android (`start_activity`, Chaquopy)](https://toga.beeware.org/en/stable/reference/platforms/android/) — **HIGH**  
- [py-pdf/pypdf — issues de memória / content streams grandes](https://github.com/py-pdf/pypdf/issues) — **MEDIUM** (casos específicos)  
- [PyMuPDF — retenção de memória com `get_pixmap`](https://github.com/pymupdf/PyMuPDF/issues/3625) — **MEDIUM**  
- [Dpdf — flatten vs rasterize (diferença de modelo mental)](https://www.dpdf.com/blog/flatten-vs-rasterize-pdf) — **MEDIUM** (educativo, não normativo legal)  
- [PDF Tools — camadas ocultas / redacção](https://www.pdf-tools.com/pdf-knowledge/the-hidden-layers-of-pdf-redaction/) — **MEDIUM**  
- [Liberation Fonts — LICENSE (SIL OFL)](https://github.com/liberationfonts/liberation-fonts/blob/main/LICENSE) — **HIGH** para licenciamento da família Liberation  
- [BeeWare Toga — discussão / issues sobre diálogo de ficheiros no Android](https://github.com/beeware/toga/discussions/1990) — **MEDIUM** (verificar versão atual do projeto)  
- [Relato: paths Android `briefcase run`](https://errorism.dev/issues/beeware-briefcase-no-such-file-or-directory-when-run-in-android) — **LOW** (terceiro; útil como sintoma)

## Play Store vs sideload (breve)

- **Ambos** exigem **assinatura** do APK/AAB para instalação útil; a documentação Briefcase sublinha que o output de `briefcase package` **deve ser assinado** quer para Play quer para carregamento direto.  
- **Play Store:** `version_code` monotónico, políticas de dados/privacidade (app “local” ainda pode precisar de declaração clara de ausência de rede se removerem `INTERNET` — hoje o template Briefcase menciona concessão automática de `INTERNET`; validar implicações de política).  
- **Sideload:** utilizador ativa “fontes desconhecidas”; menor fricção de revisão mas **mesmos** desafios técnicos de **storage** e **assinatura**. Não é requisito do milestone; só **não confundir** sideload com “dispensa de cuidados de I/O ou segurança”.

---
*Pitfalls research for: marca d’água local Android (Python/BeeWare, PDF endurecido)*  
*Researched: 2026-05-12*
