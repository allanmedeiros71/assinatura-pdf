# MarcaJá

Aplicativo **Android** em **Python** ([BeeWare](https://beeware.org/)) para aplicar **marca d’água em texto** a **PDFs e imagens** no próprio **smartphone** — **100% local**, sem servidor nem login. O objetivo é preparar **arquivos** para enviar a terceiros (seguradoras, bancos, etc.) com menos risco de reutilização indevida do original.

## Estado do projeto

- **Marco atual:** v1.0 — *Execução MVP* (fases 1 a 5 no roadmap).
- **Código do app BeeWare:** pacote `src/marcaja` com Toga/Briefcase; ver secção **Desenvolvimento** abaixo.
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

## Desenvolvimento

Pré-requisitos: **Python 3.12**, **JDK 17**, **Android SDK** (variável `ANDROID_HOME` ou `ANDROID_SDK_ROOT`), e venv com dependências do projeto.

```bash
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e ".[dev]"
briefcase create android      # primeira vez / após mudar recursos nativos
briefcase run android         # smoke no emulador ou dispositivo
```

O fluxo de UI completo no dispositivo é **verificação manual** (tela única, botões **Ok** e **Sair**). Em desktop Linux, `python -m marcaja` ou o entrypoint que o Briefcase gerar pode não estar disponível sem backend GTK; priorize `briefcase run` na plataforma alvo.

## Fontes

O equivalente open source a Arial usado no projeto é **Liberation Sans**, licenciada sob a **SIL Open Font License (OFL)**. O arquivo empacotado no repositório é:

`src/marcaja/resources/fonts/LiberationSans-Regular.ttf`

## Estrutura útil do repositório

```text
.
├── README.md              # este arquivo
├── pyproject.toml         # Briefcase / Toga
├── src/marcaja/           # código do app (app.py, recursos)
├── projeto.md             # especificação original
├── .planning/             # planejamento GSD (projeto, roadmap, requisitos, pesquisa)
├── .cursor/rules/         # regras do Cursor (ex.: pt-BR padrão)
└── .planning/phases/      # contexto por fase (ex.: 01-CONTEXT.md)
```

## Idioma

Texto de produto e UI em **português do Brasil (pt-BR)** — ver `.cursor/rules/language-pt-br.mdc`.

## Licença

Metadados do app em `pyproject.toml` usam **MIT** para o pacote Python do MarcaJá. A fonte **Liberation Sans** segue a **SIL Open Font License (OFL)** (ver pasta `src/marcaja/resources/fonts/`).

---

**MarcaJá** — marca d’água rápida antes de compartilhar documentos.
