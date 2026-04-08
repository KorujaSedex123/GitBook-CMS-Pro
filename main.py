import os
import sys
from dotenv import load_dotenv, set_key
from rich.console import Console
from rich.panel import Panel
import questionary

# Força o terminal do Windows a ler caracteres especiais e cores
if os.name == 'nt':
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

# Importações dos seus módulos internos
from cms_gitbook import cms_gitbook
from extrator_api import extrator_api
from qa_auditor import qa_auditor

console = Console()

ARTE_ASCII = """[bold cyan]
  ____ _ _   ____              _    
 / ___(_) |_| __ )  ___   ___ | | __
| |  _| | __|  _ \ / _ \ / _ \| |/ /
| |_| | | |_| |_) | (_) | (_) |   < 
 \____|_|\__|____/ \___/ \___/|_|\_\\
      CMS PRO - RPG FORGEMASTER
[/bold cyan]"""

def setup_inicial():
    """Verifica se as chaves existem. Se não, faz a entrevista usando input nativo (aceita Ctrl+V)"""
    env_path = ".env"
    
    if not os.path.exists(env_path):
        open(env_path, 'w').close()
        
    load_dotenv(env_path)
    
    gitbook_token = os.getenv("GITBOOK_TOKEN")
    github_token = os.getenv("GITHUB_TOKEN")
    github_repo = os.getenv("GITHUB_REPO")
    
    if not gitbook_token or not github_token or not github_repo:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(ARTE_ASCII)
        console.print(Panel.fit(
            "[bold green]✨ BEM-VINDO AO GITBOOK CMS PRO ✨[/bold green]\n"
            "[dim]Parece que é sua primeira vez aqui. Vamos configurar seu universo![/dim]",
            border_style="green"
        ))
        
        # Usamos console.input() no lugar de questionary para garantir o Ctrl+V
        if not gitbook_token:
            console.print("\n[bold cyan]1. Token do GitBook[/bold cyan]")
            novo_gb = console.input("Cole o seu Token do GitBook [dim](Ctrl+V ou Botão Direito)[/dim]: ")
            if novo_gb: set_key(env_path, "GITBOOK_TOKEN", novo_gb.strip())
            
        if not github_token:
            console.print("\n[bold cyan]2. Token do GitHub[/bold cyan]")
            novo_gh = console.input("Cole o seu Token do GitHub [dim](Ctrl+V ou Botão Direito)[/dim]: ")
            if novo_gh: set_key(env_path, "GITHUB_TOKEN", novo_gh.strip())
            
        if not github_repo:
            console.print("\n[bold cyan]3. Repositório do GitHub[/bold cyan]")
            novo_repo = console.input("Digite seu repositório [dim](Ex: Bruno/ExtincaoRPG)[/dim]: ")
            if novo_repo: set_key(env_path, "GITHUB_REPO", novo_repo.strip())
            
        console.print("\n[bold green]✅ Configuração concluída e salva com segurança![/bold green]")
        console.input("[dim]Pressione Enter para entrar no HUB Principal...[/dim]")
        
        load_dotenv(env_path, override=True)

def main():
    setup_inicial()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(ARTE_ASCII)
        console.print(Panel.fit(
            "[bold blue]Central de Ferramentas - Extinção & DungeonMint[/bold blue]", 
            border_style="blue"
        ))
        
        escolha = questionary.select(
            "Qual módulo você deseja acessar?",
            choices=[
                questionary.Choice("📝 CMS (Forja de Monstros e Escrita)", value="cms"),
                questionary.Choice("📦 Extrator (Gerar Web App Offline)", value="extrator"),
                questionary.Choice("📊 QA Auditor (Checagem e Balanceamento)", value="qa"),
                questionary.Separator(),
                questionary.Choice("❌ Sair do Sistema", value="sair")
            ],
            pointer="👉"
        ).ask()

        if escolha == "sair" or escolha is None:
            console.print("[yellow]Desconectando do HUB...[/yellow]")
            break
            
        try:
            if escolha == "cms":
                cms_gitbook.main()
            elif escolha == "extrator":
                extrator_api.main()
            elif escolha == "qa":
                qa_auditor.main()
        except KeyboardInterrupt:
            console.print("\n[yellow]Módulo interrompido pelo usuário.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]❌ Erro no módulo: {e}[/red]")
        
        console.input("\n[dim]Pressione Enter para voltar ao Hub Principal...[/dim]")

if __name__ == "__main__":
    main()