# MarcaJá

Aplicativo **Android** em **Python** ([BeeWare](https://beeware.org/)) para aplicar **marca d’água em texto** a **PDFs e imagens** no próprio **smartphone** — **100% local**, sem servidor nem login. O objetivo é preparar **arquivos** para enviar a terceiros (seguradoras, bancos, etc.) com menos risco de reutilização indevida do original.

## Estado do projeto

- **Marco atual:** v1.0 — *Execução MVP* (fases 1 a 5 no roadmap).
- **Código do app BeeWare:** em arranque; o repositório contém sobretudo **planejamento** (GSD) e a especificação em `projeto.md`.
- **Documentação de produto e requisitos:** `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `projeto.md`.
- **Roadmap e fases:** `.planning/ROADMAP.md` · contexto da Fase 1: `.planning/phases/01-fundacao-beeware-tela-principal/01-CONTEXT.md`.
- **Pesquisa (stack, riscos, arquitetura):** `.planning/research/`.

## O que o MVP deve fazer

- Uma **única tela** (Material / Android moderno).
- **Vários** PDFs ou imagens de cada vez, texto da marca até **200** caracteres, botões **Ok** e **Sair**.
- Marca com **ângulo** e **tamanho** pensados para o layout da página; **várias linhas** se o texto for longo.
- Saída em **PDF** com texto **difícil de copiar** e **sem OCR útil** para o conteúdo original (expectativas realistas documentadas no planejamento).
- Fonte **Arial** ou equivalente **open source** (ex.: Liberation Sans) empacotada no app.

## Stack previsto

| Área | Escolha |
|------|---------|
| Linguagem | Python 3.12+ |
| UI / app nativa | [Toga](https://toga.beeware.org/) |
| Empacotamento | [Briefcase](https://briefcase.beeware.org/) (Android) |
| PDF / imagem | Ver `.planning/research/STACK.md` (incl. notas sobre motor no Android) |

## Como desenvolver (quando o projeto BeeWare existir)

Os passos concretos (`briefcase new`, `briefcase dev android`, etc.) serão definidos no **plano da Fase 1**. Até lá:

1. Lê `.planning/phases/01-fundacao-beeware-tela-principal/01-CONTEXT.md` e `.planning/research/SUMMARY.md`.
2. Segue o fluxo GSD do repositório: por exemplo `/gsd-plan-phase 1` após discussão da fase.

## Estrutura útil do repositório

```text
.
├── README.md              # este arquivo
├── projeto.md             # especificação original
├── .planning/             # planejamento GSD (projeto, roadmap, requisitos, pesquisa)
├── .cursor/rules/         # regras do Cursor (ex.: pt-BR padrão)
└── .planning/phases/      # contexto por fase (ex.: 01-CONTEXT.md)
```

## Idioma

Texto de produto e UI em **português do Brasil (pt-BR)** — ver `.cursor/rules/language-pt-br.mdc`.

## Licença

*A definir* — escolher licença (ex. MIT) quando o código público estiver estável.

---

**MarcaJá** — marca d’água rápida antes de compartilhar documentos.
