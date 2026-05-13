# Walking Skeleton — MarcaJá

**Fase:** 1  
**Gerado:** 2026-05-12

## Capacidade ponta a ponta provada

O usuário **instala e abre** o app Android gerado por **Briefcase/Toga** (`marcaja`), vê **uma tela** com título **MarcaJá**, texto placeholder, botões **Ok** e **Sair**, e **Sair** encerra o aplicativo. Não há persistência nem backend — apenas ciclo de vida app + UI nativa.

## Decisões arquiteturais

| Decisão | Escolha | Motivo |
|---------|---------|--------|
| Framework app | BeeWare **Toga** + **Briefcase** | Requisito do produto (PLAT-01) |
| Plataforma alvo | **Android** (Gradle) | Escopo v1; iOS fora |
| Camada de dados | *Nenhuma na Fase 1* | App local; sessão/arquivos na Fase 2+ |
| Layout | `MainWindow` + `Box` vertical + faixa de botões | `01-UI-SPEC.md` + ARCHITECTURE |
| Fonte de marca | **Liberation Sans** (TTF, OFL) em `src/marcaja/resources/fonts/` | WM-07; uso renderização nas fases 3–5 |
| Identificação do pacote | `bundle` + app `marcaja` (ver `pyproject.toml`) | D-01 |

## Stack tocada na Fase 1

- [x] Scaffold Briefcase (`pyproject.toml`, `src/marcaja`)
- [x] Uma tela real (`MainWindow`) com interação mínima (Ok stub, Sair encerra)
- [ ] “Base de dados” — **N/A** (substituído por ausência de persistência intencional)
- [x] UI interativa básica
- [x] Execução documentada (`README.md`: `briefcase run android` quando ambiente pronto)

## Fora do escopo do skeleton

- Seleção de arquivos, lista, campo 200 caracteres (Fase 2)
- Motor PDF / cache (Fase 3)
- Marca diagonal e lote (Fase 4)
- PDF endurecido e compartilhar (Fase 5)

## Próximos fatias

- **Fase 2:** lote + texto da marca na mesma `MainWindow`
- **Fase 3:** pipeline PDF + cache
- **Fase 4:** geometria + processamento em série
- **Fase 5:** endurecimento + export + erros
