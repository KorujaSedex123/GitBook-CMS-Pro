import os
import sys
import subprocess
from rich.console import Console
from rich.panel import Panel
import questionary

console = Console()

def executar_ferramenta(caminho_script):
    """Executa o script selecionado usando o mesmo ambiente virtual (venv)"""
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        # sys.executable garante que ele use o Python do venv ativado
        subprocess.run([sys.executable, caminho_script])
    except KeyboardInterrupt:
        console.print("\n[yellow]Execução interrompida pelo usuário.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Erro ao executar {caminho_script}: {e}[/red]")
    
    # Pausa antes de retornar ao Hub Principal
    console.input("\n[dim]Pressione Enter para voltar ao Hub Principal...[/dim]")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel.fit(
            "[bold blue]GitBook API Hub[/bold blue]\n[dim]Central de Ferramentas - Extinção & DungeonMint[/dim]", 
            border_style="blue"
        ))
        
        escolha = questionary.select(
            "Qual módulo você deseja acessar?",
            choices=[
                questionary.Choice("📝 CMS (Forja de Monstros e Escrita)", value="cms_gitbook/cms_gitbook.py"),
                questionary.Choice("📦 Extrator (Gerar Web App Offline)", value="extrator_api/extrator_api.py"),
                questionary.Choice("📊 QA Auditor (Checagem e Balanceamento)", value="qa_auditor/qa_auditor.py"),
                questionary.Separator(),
                questionary.Choice("❌ Sair do Sistema", value="sair")
            ],
            pointer="👉"
        ).ask()

        if escolha == "sair" or escolha is None:
            console.print("[yellow]Desconectando do HUB...[/yellow]")
            break
            
        # Normaliza o caminho para funcionar perfeitamente no Windows (\) ou Mac/Linux (/)
        caminho_correto = os.path.normpath(escolha)
        
        if os.path.exists(caminho_correto):
            executar_ferramenta(caminho_correto)
        else:
            console.print(f"[red]❌ Arquivo não encontrado: {caminho_correto}[/red]")
            console.print("[yellow]Certifique-se de que a estrutura de pastas está correta.[/yellow]")
            console.input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()