---
phase: 01
slug: fundacao-beeware-tela-principal
status: approved
shadcn_initialized: false
preset: not-applicable-toga-android
created: 2026-05-12
platform: android
toolkit: toga-briefcase
---

# Fase 01 — Contrato de UI (MarcaJá)

> Contrato visual e de interação para a **Fundação BeeWare e tela principal**. Consome decisões de `01-CONTEXT.md`, requisitos **PLAT-01**, **UI-01**–**UI-03**, **WM-07** e `STACK.md`. Stack: **Toga 0.5.x** em **Android** (Material coerente com widgets nativos), sem camada web (shadcn/Tailwind **não** se aplicam).

---

## Plataforma e design system

| Propriedade | Valor |
|-------------|--------|
| Ferramenta UI | **Toga** (BeeWare) sobre **Android** |
| Preset / DS web | **Não aplicável** (sem React/shadcn) |
| Biblioteca de componentes | Widgets **Toga** mapeados para controles **Material** do Android |
| Biblioteca de ícones | **Nenhuma** nesta fase (somente texto; ícones só se o template Briefcase já trouxer e não atrasar o escopo) |
| Fonte de marca (WM-07) | **Liberation Sans** (`.ttf`, OFL), caminho estável no repo (ex.: `resources/fonts/`) — ver `01-CONTEXT.md` D-06 |

**Idioma:** todas as strings visíveis em **pt-BR** (`.cursor/rules/language-pt-br.mdc`).

---

## Estrutura da tela (UI-01, UI-03)

Layout único (`MainWindow`), **sem onboarding**.

| Região | Conteúdo | Comportamento |
|--------|-----------|----------------|
| Topo | Título **MarcaJá** (nome do produto) | Âncora visual principal (foco hierárquico #1) |
| Centro | Placeholder curto (1–2 linhas), ex.: *"Em breve: lote e marca d’água."* | Não interativo nesta fase; substituível na Fase 2 sem mudar barra inferior |
| Inferior | Dois botões em **linha** (horizontal): **Ok** à esquerda ou primeiro; **Sair** ao lado | Sempre **visíveis** sem rolagem em telefone comum (UI-03); área tocável mínima **48×48 dp** cada |

**Hierarquia visual (dim. 2):** título *MarcaJá* → texto do placeholder → botões (peso visual maior nos botões que no placeholder, via estilo primário/secundário abaixo).

---

## Escala de espaçamento (dp)

Valores em **dp**, múltiplos de **4** (grid 4 dp). Aplicar como `padding`/`margin` entre regiões e dentro dos botões.

| Token | Valor | Uso |
|-------|-------|-----|
| xs | 4 dp | Espaço entre ícone e rótulo (futuro) |
| sm | 8 dp | Espaçamento compacto entre botões vizinhos |
| md | 16 dp | Padding lateral da tela, padding interno padrão dos botões |
| lg | 24 dp | Separação entre bloco central e faixa de botões |
| xl | 32 dp | Respiro acima do título (safe area + toolbar) |
| 2xl | 48 dp | Altura mínima tocável (alinhar com 48 dp de toque) |

**Exceções:** nenhuma fora desta escala nesta fase.

---

## Tipografia (WM-07 + legibilidade)

Fonte UI padrão: **sistema Android** via Toga (Roboto / tipografia Material) para labels da janela e botões. **Liberation Sans** fica **empacotada e documentada** nesta fase para uso **posterior** no pipeline de marca (Fases 3–5), não obrigando trocar a fonte de toda a UI nativa na Fase 1.

| Papel | Tamanho (sp) | Peso | Altura de linha |
|-------|----------------|------|------------------|
| Título (MarcaJá) | 20 | 600 | 1,25 |
| Corpo (placeholder central) | 16 | 400 | 1,5 |
| Rótulo de botão (Ok / Sair) | 16 | 600 | 1,2 |

**Escala:** 2 tamanhos distintos (16, 20) e **2 pesos** (400, 600) — dentro dos limites da dimensão Tipografia.

---

## Cor (papel semântico, alinhado Material)

Contrato em **papéis**; implementação segue tema **Material** do dispositivo (claro/escuro). Valores hex abaixo são **referência** para documentação/planos, não obrigação de cor fixa fora do sistema.

| Papel | Valor ref. | Uso (60/30/10) |
|-------|------------|----------------|
| Dominante (~60%) | Superfície / fundo (`#FFFBFE` ref. tema claro) | Fundo da janela |
| Secundário (~30%) | Container de conteúdo / superfície elevada (`#F3F4F6` ref.) | Área do placeholder, se usar cartão |
| Acento (~10%) | Cor primária Material (`#6750A4` ref. dinâmico) | **Somente** preenchimento do botão **Ok** (CTA primária) |
| Contraste | Texto primário/on-surface | Título e placeholder |
| Destrutivo | Cor de erro Material | **Não** usada nesta fase (nenhuma ação destrutiva de dados; **Sair** não usa cor destrutiva) |

**Acento reservado para:** exclusivamente o botão **Ok** (estado default). **Não** usar acento em **Sair**, texto do placeholder nem título (título usa cor “on-surface”, não acento).

---

## Contrato de textos (copy)

| Elemento | Texto / regra |
|----------|----------------|
| Título da janela / topo | **MarcaJá** |
| Placeholder central (exemplo aprovado) | *"Em breve: lote e marca d’água."* (pode ajustar microcopy dentro do mesmo tom, pt-BR) |
| Botão primário (UI-03) | **Ok** — rótulo **fixo** por requisito; semântica: *confirmar* e manter o app pronto para evolução da Fase 2 (nesta fase sem processamento) |
| Botão sair (UI-03) | **Sair** — encerra o app corretamente no ciclo de vida Android (**D-05**) |
| Estado vazio “duro” | Não aplicável: o centro sempre mostra o placeholder |
| Estado de erro | Fora do escopo da Fase 1; na Fase 5 usar padrão *problema + próximo passo* |
| Confirmação destrutiva | Não há remoção de dados nesta fase; **Sair** sem diálogo obrigatório (pode seguir padrão Toga/Android; se plataforma exigir confirmação no futuro, tratar na plan/exec) |

**Nota de alinhamento (dim. 1):** o rótulo **Ok** é **exigência explícita** de **UI-03** e `01-CONTEXT.md` D-04, não um “OK” genérico substituível; o contrato amarra **semântica** + **string visível** para o planner/executor.

---

## Componentes Toga (orientação de implementação)

| UI | Widget sugerido (Toga) | Notas |
|----|-------------------------|--------|
| Janela + layout | `MainWindow` + `toga.Box` vertical | Uma coluna: título → expansão do centro → `toga.Box` horizontal para botões |
| Título | `toga.Label` com estilo de cabeçalho / fonte maior | Acessível como texto, não só decoração |
| Centro | `toga.Label` (multiline permitido) | `flex=1` para empurrar botões para baixo |
| Ok | `toga.Button` estilo **primário** (preenchido) | `on_press` stub: log ou `pass` documentado até Fase 2 |
| Sair | `toga.Button` estilo **secundário** / outline | `on_press` → encerrar app (`app.exit()` ou equivalente documentado no plano) |

---

## Segurança de registry (dim. 6)

| Registry | Blocos | Gate |
|----------|--------|------|
| shadcn / npm UI blocks | **Nenhum** | **Não aplicável** — app não usa pipeline de componentes web |
| Terceiros (marketplace de blocos) | **Nenhum** | **Não aplicável** |

**Veredito dim. 6:** sem registros terceiros; contrato limita-se a **Toga + sistema Android**.

---

## Rastreio de requisitos

| ID | Cobertura neste contrato |
|----|---------------------------|
| PLAT-01 | Toga/Briefcase/Android implícito em todo o documento |
| UI-01 | Uma tela, sem onboarding |
| UI-02 | Papéis Material + widgets nativos Toga |
| UI-03 | Ok + Sair visíveis na base |
| WM-07 | Liberation Sans empacotada + documentação (README/PROJECT) — uso pleno da fonte na UI nativa opcional Fase 1 |

---

## Assinatura do checker (revisão inline)

| Dimensão | Resultado | Notas |
|----------|------------|--------|
| 1 Copywriting | **PASS** | Strings específicas pt-BR; **Ok**/**Sair** travados por requisito |
| 2 Visuals | **PASS** | Foco = título; hierarquia declarada |
| 3 Cor | **PASS** | Acento só no Ok; sem “todos os interativos” |
| 4 Tipografia | **PASS** | 2 tamanhos (16, 20 sp); 2 pesos (400, 600) |
| 5 Spacing | **PASS** | Só múltiplos de 4 dp na escala |
| 6 Registry | **PASS** | Sem terceiros web |

**Aprovação:** aprovado em **2026-05-12** (orquestrador `/gsd-ui-phase 1`, verificação inline; agentes `gsd-ui-researcher` / `gsd-ui-checker` indisponíveis no projeto).

---

## UI-SPEC COMPLETE

Contrato pronto para `/gsd-plan-phase 1`.
