# Phase 2: Sessão, lista e texto da marca - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-15  
**Phase:** 2-Sessão, lista e texto da marca  
**Areas discussed:** layout, adicionar arquivos, lista editável, campo da marca, botão Ok

---

## Layout da tela única

| Option | Description | Selected |
|--------|-------------|----------|
| add_lista_texto | Botão adicionar → lista → campo marca → Ok/Sair | ✓ |
| lista_add_texto | Lista com adicionar no topo → campo → Ok/Sair | |
| texto_lista | Campo marca antes da lista | |

| Option | Description | Selected |
|--------|-------------|----------|
| flex_scroll | Área central flexível com rolagem na lista | ✓ |
| altura_fixa | Lista altura fixa ~40% | |
| voce_decide | Planner decide desde que Ok/Sair visíveis | |

| Option | Description | Selected |
|--------|-------------|----------|
| msg_curta | Mensagem "Nenhum arquivo selecionado" | ✓ |
| so_botao | Só botão adicionar | |
| placeholder_igual | Manter placeholder Fase 1 até primeiro arquivo | |

| Option | Description | Selected |
|--------|-------------|----------|
| texto_marca | Rótulo "Texto da marca d'água" | |
| marca | Rótulo "Marca d'água" | ✓ |
| sem_rotulo | Sem rótulo | |

**User's choice:** Ordem add → lista → texto; lista flex com scroll; estado vazio com mensagem; rótulo **Marca d'água**.

---

## Adicionar arquivos

| Option | Description | Selected |
|--------|-------------|----------|
| adicionar | "Adicionar arquivos" | |
| selecionar | "Selecionar arquivos" | |
| adicionar_pdf_img | "Adicionar PDF ou imagem" | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| acumular | Novos arquivos acumulam no lote | ✓ |
| substituir | Cada seleção zera a lista | |
| perguntar | Diálogo adicionar vs substituir | |

| Option | Description | Selected |
|--------|-------------|----------|
| pdf_png_jpeg | PDF, PNG, JPEG apenas | ✓ |
| pdf_todas_img | PDF + qualquer imagem do sistema | |
| voce_decide | Mínimo PDF+PNG+JPEG no plano | |

| Option | Description | Selected |
|--------|-------------|----------|
| sem_mudanca | Cancelar picker sem mensagem | ✓ |
| toast | "Seleção cancelada" | |

**User's choice:** Botão explícito PDF/imagem; acumular; tipos restritos; cancelamento silencioso.

---

## Lista editável

| Option | Description | Selected |
|--------|-------------|----------|
| nome_arquivo | Só nome | |
| nome_tipo | Nome + tipo (PDF/PNG/…) | ✓ |
| nome_tamanho | Nome + tamanho | |

| Option | Description | Selected |
|--------|-------------|----------|
| botao_remover | Botão/ícone remover por linha | ✓ |
| toque_longo | Toque longo + confirmar | |
| ambos | Lixeira + confirmação se último | |

| Option | Description | Selected |
|--------|-------------|----------|
| permitir | Duplicatas permitidas | |
| ignorar | Ignorar silenciosamente duplicatas | ✓ |
| avisar | Ignorar e avisar | |

| Option | Description | Selected |
|--------|-------------|----------|
| ellipsis | Truncar com reticências | ✓ |
| quebra | Quebra de linha | |
| scroll_horizontal | Scroll horizontal no nome | |

**User's choice:** Nome+tipo; remover explícito; sem duplicatas; ellipsis em nomes longos.

---

## Campo da marca (200 caracteres)

| Option | Description | Selected |
|--------|-------------|----------|
| bloquear | Bloquear digitação além de 200 | ✓ |
| truncar | Truncar colagem | |
| bloquear_e_truncar | Bloquear + truncar colagem | |

| Option | Description | Selected |
|--------|-------------|----------|
| contador_direita | Contador N/200 à direita | ✓ |
| contador_rotulo | Contador no rótulo | |
| so_vermelho | Só destaque vermelho em 200 | |

| Option | Description | Selected |
|--------|-------------|----------|
| multilinha | 2–4 linhas visíveis | ✓ |
| uma_linha | Uma linha | |
| voce_decide | Planner decide | |

| Option | Description | Selected |
|--------|-------------|----------|
| exemplo | Placeholder com exemplo de uso | ✓ |
| generico | "Digite o texto…" | |
| vazio | Sem placeholder | |

**User's choice:** Bloquear em 200; contador N/200; multilinha; placeholder com exemplo.

---

## Botão Ok (esta fase)

| Option | Description | Selected |
|--------|-------------|----------|
| validar_dialog | Validar + diálogos pt-BR; sucesso = "em breve" | ✓ |
| validar_silencioso | Validar só em log | |
| noop | Stub até Fase 4 | |
| desabilitar | Ok desabilitado até válido | |

| Option | Description | Selected |
|--------|-------------|----------|
| erro_obrigatorio | Texto vazio → erro | ✓ |
| permitir | Texto vazio permitido | |
| so_se_sem_arquivos | Só validar lista | |

| Option | Description | Selected |
|--------|-------------|----------|
| erro_lista | Sem arquivos → mensagem | ✓ |
| desabilitar_previo | Ok desabilitado | |

| Option | Description | Selected |
|--------|-------------|----------|
| dialog_em_breve | Diálogo: processamento na próxima etapa | ✓ |
| nada | Sem feedback | |
| log_only | Só log | |

**User's choice:** Validação com diálogos; texto e lista obrigatórios; sucesso parcial informa próxima etapa.

---

## Claude's Discretion

- Widgets Toga, microcopy fino dos diálogos, detalhe de colagem >200 chars, normalização de paths Android.

## Deferred Ideas

- Processamento PDF, marca diagonal, export — fases 3–5.
- Substituir lote / Ok desabilitado — não escolhidos.
