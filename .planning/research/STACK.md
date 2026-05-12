# Stack Research

**Domain:** App Android local em Python (BeeWare/Briefcase/Toga) para marca d’água em lote em PDFs/imagens, com saída em PDF “endurecido” (restrições de cópia, sem texto/OCR útil).

**Researched:** 2026-05-12

**Confidence:** **MEDIUM–HIGH** para BeeWare/Toga/Briefcase e ambiente Android (documentação oficial + PyPI). **MEDIUM** para pipeline PDF no dispositivo: **PyMuPDF não consta** no índice público de pacotes nativos da Chaquopy; a recomendação assume validação empírica no primeiro ciclo de `briefcase build android` ou plano B explícito abaixo.

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| **Python** | **3.12.x** (mínimo **3.10** exigido pelo Briefcase 0.4.x) | Linguagem única do app e do empacotamento | Alinha `requires_python` do Briefcase 0.4.2, Toga 0.5.x e PyPI atual; 3.12 é bom equilíbrio de suporte Chaquopy/Briefcase e bibliotecas. Evitar microversões exóticas: usar a mesma série no **build machine** que o target do app (Chaquopy exige major.minor iguais no `buildPython`). |
| **Briefcase** | **0.4.2** (PyPI, maio/2026) | Empacotar app BeeWare em APK/AAB Android | Versão atual com `requires_python >=3.10`; documentação oficial cobre Gradle, Java 17, SDK e `pyproject.toml`. |
| **Toga** | **0.5.4** | UI nativa (widgets, file picker, progresso) | Kit oficial BeeWare para Android; combina com Rubicon para JNI quando precisar de APIs Android não expostas pelo Toga. |
| **rubicon-java** | **0.2.6** | Bridge Python ↔ JVM/Android | Necessário para **fallback** usando `android.graphics.pdf.PdfRenderer` se PyMuPDF não empacotar no Android. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **PyMuPDF** (`import fitz`) | **1.27.2.x** (PyPI `pymupdf`) | Abrir PDF, rasterizar páginas, desenhar marca d’água vetorial/raster, gravar PDF imagem-only, ajustar permissões, remover camadas de texto/OCR | **Motor principal em desktop** e *se* o wheel instalar no build Android. É a forma mais simples de cumprir “sem texto copiável / sem OCR útil” via **flatten para imagem** + opções de segurança. |
| **pypdf** | **6.11.x** | Permissões (`/Encrypt`), merge de PDFs leves, remoção de anexos/metadata, operações estruturais sem raster | Sempre útil como camada complementar (p.ex. unificar saída, reforçar flags). Bom candidato a **100% Chaquopy** (puro Python). |
| **Pillow** | **12.2.x** | Decodificar JPEG/PNG/WebP, compor marca d’água, redimensionar, preparar páginas raster | Entrada de **imagens** e etapa de composição; wheels **Pillow** existem no repositório nativo Chaquopy (`pypi-13.1/pillow/`). |
| **img2pdf** | **0.6.3** | Montar PDF **somente a partir de imagens** (sem passar por modelo de texto) | Complementa Pillow quando o pipeline for “bitmap por página → PDF”; puro Python, tende a empacotar bem. |
| **reportlab** | **4.5.x** | Gerar PDFs vetoriais simples ou capas/calcos | **Opcional**: útil se quiser desenhar marca d’água vetorial em páginas brancas ou PDFs mínimos; **não** use como leitor/renderer de PDFs arbitrários de terceiros (use PyMuPDF ou fluxo raster). |
| **fonte Liberation Sans / Arimo** | Arquivos `.ttf` embarcados no app | Substituto open source de Arial | Empacotar TTF no projeto e carregar explicitamente no desenhista (PyMuPDF ou ReportLab); não depender de fontes do sistema Android para consistência. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| **JDK 17** | Gradle / Android toolchain | Briefcase Android documenta **Java 17**; definir `JAVA_HOME`. |
| **Android SDK** + **cmdline-tools 19.x** | `briefcase build/run android` | Definir `ANDROID_HOME` (ou `ANDROID_SDK_ROOT`, hoje tratado como legado). |
| **pip ≥ 24.3** + **venv** | Alinhar com dependências do próprio Briefcase | Criar venv dedicada; instalar Briefcase dentro dela antes de `briefcase create android`. |
| **Android Studio** (opcional mas recomendado) | Depurar Gradle, Logcat, inspecionar APK | Útil quando dependências Python nativas falham no empacotamento. |

## Installation

```bash
# --- Ambiente Python (macOS/Linux; no Windows usar py -3.12) ---
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

python -m pip install -U pip setuptools wheel
python -m pip install "briefcase==0.4.2" "toga==0.5.4"

# Dependências de aplicação (ajuste pins no pyproject.toml do Briefcase)
python -m pip install \
  "pymupdf>=1.27.2,<1.28" \
  "pypdf>=6.11,<7" \
  "Pillow>=12.2,<13" \
  "img2pdf>=0.6.3,<0.7" \
  "reportlab>=4.5,<4.6" \
  "rubicon-java>=0.2.6,<0.3"

# --- Projeto BeeWare (a partir do diretório do app) ---
briefcase new   # se greenfield; ou apenas:
briefcase create android
briefcase run android
briefcase package android -p aab    # Play Store
# briefcase package android -p apk  # sideload
```

**Android / máquina de build**

1. Instalar **JDK 17** e apontar `JAVA_HOME`.
2. Instalar **Android SDK** (APIs alinhadas ao `min_os_version` do app) e **Command-line Tools** revisão **19**+.
3. Garantir que o Python usado no PATH para o Gradle/Chaquopy é **o mesmo major.minor** configurado para o app (ver documentação Chaquopy: `buildPython` se necessário).
4. Em Apple Silicon, ABI típica para emulador: `arm64-v8a` (e `x86_64` se for testar em emulador Intel); Briefcase/Chaquopy herdam políticas de ABI do template Gradle.

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| PyMuPDF como motor de PDF | **Somente pypdf + Pillow + img2pdf** | Quando `pymupdf` **falhar** no `pip`/Chaquopy no Android: aí o fluxo honesto é obter **bitmaps por página** via **`android.graphics.pdf.PdfRenderer`** (JNI com **rubicon-java**) + marca d’água Pillow + montagem **img2pdf**, e usar **pypdf** só para metadados/permisões em cima do PDF final. |
| Toga | **Kivy + python-for-android** | Fora do escopo do projeto (requisito BeeWare); só faria sentido se o requisito de stack mudasse. |
| Pillow para imagens | **OpenCV** (`opencv-python` no Chaquopy) | Overkill para marca d’água; aumenta tamanho do APK e complexidade. Considerar só se precisar de CV pesado. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **PyPDF2** (pacote antigo) | Consolidação no **pypdf**; risco de confusão de imports e versões. | **pypdf** 6.x |
| **pdfrw**, **pyPdf** legados | Manutenção fraca; lacunas em PDF modernos e encriptação. | **pypdf** + **PyMuPDF** |
| **pdf2image** / **poppler-utils** no Android | Dependem de binário **poppler** no sistema — **não** aplicável ao runtime Chaquopy/Briefcase. | PyMuPDF raster ou **PdfRenderer** + Pillow |
| **OCR como “remoção de OCR”** (Tesseract etc.) | O requisito é **não fornecer** camada OCR útil, não “ocrar de novo”. | Rasterizar/remover content streams de texto |
| **“Só criptografar com senha”** como fim | Usuário final não deve depender de senha; não substitui ausência de texto selecionável. | PDF imagem-only + flags de permissão (`/P`) coerentes |
| **PyMuPDF no Android sem verificação** | **Não aparece** em https://chaquo.com/pypi-13.1/ como pacote nativo pré-compilado; issues públicas relatam falha de instalação via pip no Chaquopy. | Validar cedo; se bloquear, ativar fallback **PdfRenderer + Pillow + img2pdf + pypdf** |

## Stack Patterns by Variant

**Se PyMuPDF empacotar no Android (cenário ideal):**

- Abrir cada PDF com `fitz.open`, iterar páginas, `get_pixmap` com matriz de escala controlada por DPI alvo, redesenhar marca d’água com `insert_text`/`insert_image` **antes** ou **depois** da flatten conforme desenho, e salvar com política **sem texto selecionável** (pipeline baseado em imagem + remoção de fonts/text objects).
- Usar **pypdf** como pós-processador opcional para merge em lote e harmonizar dicionário de encriptação/permissões.

**Se PyMuPDF *não* empacotar (cenário provável sem wheel custom):**

- Caminho **híbrido BeeWare**: de Python, via **rubicon-java**, instanciar `PdfRenderer` sobre `ParcelFileDescriptor`, renderizar cada página em `Bitmap`, converter para `Image` Pillow, aplicar marca d’água, exportar páginas com **img2pdf**, depois **pypdf** para `encrypt`/`UserAccessPermissions` (copiar/colar desabilitados) e saneamento de metadados.
- Manter o mesmo código de marca d’água em Pillow nos dois cenários para consistência visual.

**Para imagens de entrada:**

- Pillow para normalização de modo/cor e DPI; em seguida tratar como “página única” no mesmo pipeline de exportação PDF.

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| **briefcase 0.4.2** | **Python ≥3.10** | PyPI oficial; alinhar com Chaquopy (3.10–3.14 disponíveis na série 17.x conforme doc Chaquopy). |
| **toga 0.5.4** | **Python ≥3.10** | Manter versões Toga/Briefcase da mesma “onda” BeeWare (checar release notes se atualizar um sem o outro). |
| **pymupdf ~1.27** | **Python ≥3.10** | Confirmar ABI **arm64-v8a** no APK; conflitos raros com outras libs nativas — isolar import/falha graciosa. |
| **pypdf 6.x** | **Python ≥3.9** | API estável; ler notas de migração se vier de PyPDF2. |
| **Pillow 12.x** | **Python ≥3.10** | No Android, respeitar limites de memória: não manter todos `Image` de um lote gigante em RAM. |
| **Chaquopy (via Briefcase)** | **Android Gradle Plugin 7.3.x–9.2.x**, **minSdk ≥24** | Conforme documentação Chaquopy 17.x; Briefcase gerencia template, mas customizações Gradle devem respeitar esse intervalo. |

## Sources

- **Context7** — `/beeware/briefcase`: tópicos “Android packaging”, `pyproject.toml` Android, requisitos de ambiente (Java 17, SDK, wheels).
- **PyPI JSON** — `https://pypi.org/pypi/briefcase/json` (versão **0.4.2**, `requires_python >=3.10`), versões correntes de `toga`, `pymupdf`, `pypdf`, `Pillow`, `reportlab`, `img2pdf`, `rubicon-java`.
- **BeeWare** — `https://docs.beeware.org/` (hub de documentação); Briefcase: `https://briefcase.readthedocs.io/` / `https://briefcase.beeware.org` (referenciados no PyPI).
- **Chaquopy** — `https://chaquo.com/chaquopy/doc/current/android.html` (plugin Gradle 17.x, Python 3.10–3.14, `pip install`, `buildPython`, ABIs, minSdk). Lista de pacotes nativos: `https://chaquo.com/pypi-13.1/` (**sem entrada `pymupdf/`** — verificado em 2026-05-12).
- **Comunidade / issues** — Discussões GitHub Chaquopy/PyMuPDF sobre wheels Android (confiança **MEDIUM**: orienta risco, não substitui teste de build).

---
*Stack research for: Marca d’água local (Android) — PDF endurecido*

*Researched: 2026-05-12*
