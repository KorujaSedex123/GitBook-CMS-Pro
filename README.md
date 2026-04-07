# 🎲 GitBook-CMS-Pro

Um ecossistema centralizado em Python para gestão avançada, auditoria e exportação de manuais de RPG (como *EXTINÇÃO* e *DungeonMint*). Este painel conecta a API do GitBook e do GitHub para criar um pipeline de Game Design profissional, incluindo integração direta com o Foundry VTT e geração de Web Apps offline.

## 🚀 Funcionalidades (O Hub Central)

O projeto é dividido em três módulos principais, orquestrados por um Hub central (`main.py`):

* **📝 CMS & Forja de Monstros (Cloud-Native):** Criação de páginas e ameaças direto no terminal. Gera arquivos Markdown e `.json` configurados para o **Foundry VTT** e transmite os dados em Base64 diretamente para o GitHub (via REST API), ativando o Git Sync do GitBook instantaneamente.
* **📦 Codex Extractor (Web App Offline):**
    Consome a árvore de conteúdo do GitBook e compila o manual inteiro em um arquivo HTML/Tailwind offline, responsivo e com suporte a *Dark Mode*. Inclui um algoritmo em JavaScript que detecta sintaxe de RPG (ex: `2d6+2`) e os transforma em **botões roláveis de dados** interativos.
* **📊 QA & Balance Auditor:**
    Varre a API do GitBook em busca de falhas de documentação (páginas vazias, falta de arte) e extrai estatísticas de combate (PV, Defesa, Dano) de todas as ameaças, exportando um arquivo `planilha_de_balanceamento.csv` para análise de curva de dificuldade.

## 📂 Estrutura do Projeto

                GitBook-CMS-Pro/
                ├── cms_gitbook/
                │   └── cms_gitbook.py       # Motor de criação e sync com GitHub
                ├── extrator_api/
                │   └── extrator_api.py      # Motor de compilação HTML
                ├── qa_auditor/
                │   └── qa_auditor.py        # Motor de auditoria e CSV
                ├── exportacoes/             # HTMLs offline gerados
                ├── .env                     # Chaves de API (Ignorado pelo Git)
                ├── .gitignore
                ├── requirements.txt         # Dependências do projeto
                └── main.py                  # Hub Interativo (Lançador)

## ⚙️ Instalação e Configuração
1. Clone o repositório e acesse a pasta:
                
         git clone https://github.com/KorujaSedex123/GitBook-CMS-Pro.git
         cd GitBook-CMS-Pro

2. Crie e ative o Ambiente Virtual (venv):
                
                python -m venv venv
                .\venv\Scripts\activate

3. Instale as dependências:

                pip install -r requirements.txt


4. Configure as Variáveis de Ambiente:
Crie um arquivo chamado ``.env`` na raiz do projeto e adicione suas credenciais:
          

            # API do GitBook (Para o Extrator e Auditor)
            GITBOOK_TOKEN=gb_api_seu_token_aqui
            # API do GitHub (Para o CMS via Git Sync)
            GITHUB_TOKEN=ghp_seu_token_github_aqui
            GITHUB_REPO=SeuUsuario/NomeDoRepositorio



## 🎮 Como Usar
Com o ambiente virtual ativado, basta iniciar o Hub Central. A interface interativa no terminal guiará você por todas as opções.


        python main.py

Navegue com as setas do teclado ou com o mouse para selecionar o módulo desejado. Ao finalizar a execução de qualquer ferramenta, o sistema retornará magicamente ao menu principal.

## **Desenvolvido para automatizar e blindar a criação de universos de RPG.**