# 🎲 GitBook-CMS-Pro

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#)
[![Foundry VTT](https://img.shields.io/badge/Foundry%20VTT-Compatible-orange.svg)](https://foundryvtt.com)
[![GitBook](https://img.shields.io/badge/GitBook-Sync-blueviolet.svg)](https://gitbook.com)

**GitBook-CMS-Pro** é um ecossistema centralizado em Python projetado para a gestão avançada, auditoria de balanceamento e exportação de manuais de RPG (como *EXTINÇÃO* e *DungeonMint*). 

Este hub de ferramentas atua como uma ponte inteligente entre a **API do GitBook**, a **API do GitHub** e o **Foundry VTT**, estruturando um pipeline profissional e automatizado para Game Designers e criadores de conteúdo de RPG.

---

## 🚀 Funcionalidades Principais (O Hub Central)

O ecossistema é composto por três módulos independentes e altamente integrados, todos orquestrados por uma interface interativa via terminal (`main.py`):

```
                       ┌─────────────────────────┐
                       │  main.py (Hub Central)  │
                       └────────────┬────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
 📝 cms_gitbook/            📦 extrator_api/           📊 qa_auditor/
  - Forja de Monstros        - Codex Extractor          - QA & Balance
  - Sync Base64 c/ GitHub    - HTML Offline             - Auditoria de APIs
  - Ativação Git Sync        - Rolador de Dados JS      - Curva de Dificuldade (CSV)
```

### 1. 📝 CMS & Forja de Monstros (Cloud-Native)
*   **Criação Direta via Terminal:** Permite criar páginas e ameaças detalhadas diretamente pela interface de comando.
*   **Pronto para Foundry VTT:** Gera automaticamente arquivos Markdown e formatos `.json` pré-configurados para importação no Foundry VTT.
*   **Sincronização Instantânea:** Transmite os dados estruturados codificados em **Base64** diretamente para o repositório do GitHub (via GitHub REST API). Essa ação aciona automaticamente o mecanismo de *Git Sync* do GitBook, atualizando seu manual na nuvem em tempo real.

### 2. 📦 Codex Extractor (Web App Offline)
*   **Compilação Completa:** Consome toda a árvore de conteúdo e navegação configurada no GitBook.
*   **Web App Responsivo:** Compila o manual inteiro em um único arquivo HTML estilizado com Tailwind CSS, totalmente offline, responsivo e com suporte nativo a *Dark Mode*.
*   **Rolagem de Dados Interativa:** Integra um algoritmo em JavaScript que escaneia o texto em busca de sintaxe padrão de RPG (ex: `2d6+2`, `1d20+5`) e as converte automaticamente em **botões roláveis e clicáveis**, permitindo testes rápidos de dados diretamente na página.

### 3. 📊 QA & Balance Auditor
*   **Auditoria de Conteúdo:** Varre a API do GitBook para identificar gargalos e falhas de documentação, como páginas vazias ou falta de ilustrações/artes fundamentais.
*   **Auditoria de Combate:** Extrai estatísticas vitais de combate (Pontos de Vida, Defesa, Dano médio, etc.) de todas as ameaças cadastradas.
*   **Análise de Curva de Dificuldade:** Exporta os dados extraídos em um arquivo estruturado `planilha_de_balanceamento.csv`, facilitando a análise e o ajuste fino do balanceamento do sistema.

---

## 📂 Estrutura do Projeto

O repositório é organizado de forma modular para fácil manutenção e escalabilidade:

```text
GitBook-CMS-Pro/
├── cms_gitbook/
│   └── cms_gitbook.py           # Motor de criação e sincronização com GitHub
├── extrator_api/
│   └── extrator_api.py          # Motor de compilação de HTML e Web App offline
├── qa_auditor/
│   └── qa_auditor.py            # Motor de auditoria, análise de dados e exportação de CSV
├── exportacoes/                 # Direitório de saída para os HTMLs offline gerados
├── .env                         # Variáveis de ambiente e chaves secretas (Ignorado pelo Git)
├── .gitignore                   # Arquivo de exclusão do Git
├── requirements.txt             # Dependências de bibliotecas Python
└── main.py                      # Hub interativo e lançador principal
```

---

## ⚙️ Instalação e Configuração

### Pré-requisitos
*   Python 3.12 instalado em sua máquina.

### Passo 1: Clonar o Repositório
Acesse o terminal e execute os comandos abaixo para obter o código e navegar até a pasta:
```bash
git clone https://github.com/KorujaSedex123/GitBook-CMS-Pro.git
cd GitBook-CMS-Pro
```

### Passo 2: Criar e Ativar o Ambiente Virtual (`venv`)
Isso garante um ambiente isolado para o projeto e suas dependências.

*   **No Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
*   **No Linux/macOS:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### Passo 3: Instalar as Dependências
Com o ambiente virtual ativo, instale todas as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### Passo 4: Configurar as Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto e adicione suas credenciais das APIs:
```env
# API do GitBook (Utilizado pelo Codex Extractor e QA Auditor)
GITBOOK_TOKEN=gb_api_seu_token_aqui

# API do GitHub (Utilizado pelo CMS para atualizar o repositório via Git Sync)
GITHUB_TOKEN=ghp_seu_token_github_aqui
GITHUB_REPO=SeuUsuario/NomeDoRepositorio
```

---

## 🎮 Como Usar

Com seu ambiente virtual ativado e as variáveis configuradas, inicie o Hub Central interativo:

```bash
python main.py
```

### ⌨️ Interface Interativa
*   O lançador possui suporte total à navegação pelo teclado (setas direcionais) e mouse.
*   Selecione o módulo desejado pressionando `Enter`.
*   Após a conclusão das tarefas do módulo selecionado, o sistema retorna de forma transparente para o menu principal, permitindo que você continue seu fluxo de trabalho sem reiniciar a aplicação.

---

## 🛠️ Detalhes de Desenvolvimento

Este projeto foi desenhado sob medida para **automatizar e blindar a criação de universos de RPG**, diminuindo erros manuais de formatação, acelerando a publicação multiplataforma (Web, PDF, Foundry VTT) e garantindo análises numéricas precisas para um design balanceado de combates.
