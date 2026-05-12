# Especificação de Requisitos: MarcaJá

## 1. Visão Geral

- Nome do Projeto
**MarcaJá** — marca d'água rápida em PDFs e imagens no Android (app local).

- Objetivo
Eventualmente eu preciso enviar documentos em formato PDF ou foto (captura de tela) para fornecedores de serviços, ex: seguradora, concessionárias, bancos etc. Para evitar o uso indevido dos meus documentos e garantir minha segurança gostaria de uma forma rápida e ágil de fazer o upload do documento e inserir uma marca d'água com um texto informado no momento do upload.

## 2. Segurança e Autenticação

- Não há necessidade de autenticação, o sistema vai rodar localmente no smartphone

## 3. Auditoria e Logs

- Não há necessidade de auditoria e log

## 4. Gestão de Acessos e Perfis (RBAC)

- Não há necessidade de gestão de acesso e perfis

## 5. Requisitos Funcionais (RF)
- O sistema deve ter somente uma tela. Ao abrir o sistema essa tela deve ser exibida.
- A tela deve ter dois campos, um botão "Ok" e um botão "Sair"
- O sistema deve ter dois campos: 1 campo para upload de arquivos (pdf e imagens) e 1 campo para texto.
- Deve ser permitido upload de mais de um arquivo por vez
- Ao clicar no botão Ok o sistema deve inserir uma marca d'água nos arquivos enviados e disponibilizá-los para download.
- A marca d'água deve ser o texto inserido no campo texto
- O campo texto pode ter até 200 caracteres

## 6. Requisitos Não Funcionais (RNF)

- O sistema deve calcular o ângulo certo e o tamanho da fonte para inserir a marca d'água para que o resultado seja visualmente interessante.
- O ângulo da marca d'água deve ser calculado de tal forma que a inclinação do texto esteja alinhada com a inclinação da reta que liga o canto inferior esquerdo e o canto superior direito do documento.
- O tamanho da fonte do texto da marca d'água deve ser calculado de forma proporcional a ocupar toda a área que liga os cantos inferior esquerdo e superior direito.
- É permitido quebrar o texto em mais de uma linha caso este seja muito longo e o tamanho da fonte fique muito pequeno
- Devem ser usadas fontes da família Arial ou equivalente que sejam open source
- Os arquivos disponibilizados para download devem ser no formato PDF, bloqueados para copiar o texto, independentemente do formato dos arquivos de entrada.
- Deve ser removido qualquer OCR disponível

## 7. Regras de Negócio (RN)

- Nenhuma é necessária

## 8. Interface e Experiência do Usuário (UI/UX)

- O sistema deve usar UX do android com design moderno

## 9. Especificações Técnicas

- O app deve ser desenvolvido em python
- Usar BeeWare (https://beeware.org/pt/) para desenvolver o app de forma nativa para Android
