import os
import json
import requests
import base64
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
import questionary

console = Console()

def enviar_para_github(caminho_arquivo, conteudo_texto, mensagem_commit):
    """Envia um arquivo diretamente para a nuvem do GitHub via API REST"""
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO")
    
    if not token or not repo:
        console.print("[red]❌ GITHUB_TOKEN ou GITHUB_REPO não encontrados no .env![/red]")
        return False

    url = f"https://api.github.com/repos/{repo}/contents/{caminho_arquivo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # O GitHub exige que o texto viaje criptografado em Base64
    conteudo_b64 = base64.b64encode(conteudo_texto.encode('utf-8')).decode('utf-8')
    
    payload = {
        "message": mensagem_commit,
        "content": conteudo_b64
    }
    
    res = requests.put(url, headers=headers, json=payload)
    
    if res.status_code in [200, 201]:
        return True
    else:
        console.print(f"[red]❌ Erro na nuvem: {res.json().get('message')}[/red]")
        return False

def modulo_criador_bestiario():
    console.print(Panel("[bold red]☁️ Forja de Monstros na Nuvem[/bold red]", expand=False))
    
    sistema = questionary.text("Qual é o Sistema de RPG? (Ex: Extinção, D&D):").ask()
    if not sistema: return
    
    nome = questionary.text("Nome da Ameaça:").ask()
    descricao = questionary.text("Descrição Curta:").ask()
    imagem_url = questionary.text("URL da Imagem (Opcional, Enter para pular):").ask()
    
    console.print("\n[bold cyan]Estatísticas de Combate[/bold cyan]")
    pv = questionary.text("Pontos de Vida (PV):").ask()
    defesa = questionary.text("Defesa / Armadura:").ask()
    ataque = questionary.text("Ataque Principal (Ex: 2d6 Garras):").ask()
    dano = questionary.text("Dano Base:").ask()
    loot = questionary.text("Espólios / Loot:").ask()
    
    conteudo_md = f"""# {nome}

> *{descricao}*

![{nome}]({imagem_url})

---

### Atributos de Combate
* **PV (Saúde):** {pv}
* **Defesa:** {defesa}

### Ações
* **Ataque Principal:** {ataque} -> **Dano {dano}**

### Espólios
* **Loot:** {loot}

---
*Forjado direto na Nuvem via GitBook CMS Pro*
"""
    
    confirmar = questionary.confirm("🚀 Enviar monstro diretamente para a Nuvem (GitHub -> GitBook)?").ask()
    
    if confirmar:
        nome_arquivo_base = nome.replace(' ', '_').replace('/', '')
        
        # 1. Preparando o envio do Markdown (A página do Livro)
        caminho_md = f"Bestiario/{sistema}/{nome_arquivo_base}.md"
        
        # 2. Preparando o envio do JSON do Foundry VTT
        foundry_data = {
            "name": nome,
            "type": "npc",
            "img": imagem_url or "icons/svg/mystery-man.svg",
            "system": {
                "attributes": {
                    "hp": {"value": int(pv) if pv.isdigit() else 10, "max": int(pv) if pv.isdigit() else 10},
                    "ac": {"value": int(defesa) if defesa.isdigit() else 10}
                },
                "details": {
                    "biography": {"value": descricao}
                }
            }
        }
        conteudo_json = json.dumps(foundry_data, indent=4, ensure_ascii=False)
        caminho_json = f"Bestiario/{sistema}/Foundry_Tokens/{nome_arquivo_base}_foundry.json"
        
        with console.status("[bold cyan]Transmitindo para a base de dados orbital...[/bold cyan]"):
            sucesso_md = enviar_para_github(caminho_md, conteudo_md, f"Adicionando monstro: {nome}")
            sucesso_json = enviar_para_github(caminho_json, conteudo_json, f"Adicionando token VTT: {nome}")
            
        if sucesso_md and sucesso_json:
            console.print(f"\n[bold green]✅ Sucesso Absoluto![/bold green]")
            console.print(f"📖 O arquivo [cyan]{caminho_md}[/cyan] já está no repositório.")
            console.print("[dim]Abra o seu GitBook e veja a pasta e o monstro aparecerem no menu lateral sozinhos dentro de alguns segundos![/dim]\n")

def modulo_escrita_livre():
    console.print(Panel("[bold blue]☁️ Escrita Livre na Nuvem[/bold blue]", expand=False))
    
    pasta_destino = questionary.text("Nome da Pasta/Capítulo (Ex: Regras Iniciais):").ask()
    if not pasta_destino: return
    
    titulo = questionary.text("Título da Página:").ask()
    
    console.print("\n[dim]Escreva o seu conteúdo em Markdown abaixo. Digite 'FIM' em uma linha vazia para publicar.[/dim]")
    
    linhas = []
    while True:
        linha = input()
        if linha.strip().upper() == 'FIM':
            break
        linhas.append(linha)
    
    conteudo = "\n".join(linhas)
    
    if titulo and conteudo:
        nome_arquivo = titulo.replace(' ', '_').replace('/', '') + ".md"
        caminho_md = f"Escritos/{pasta_destino}/{nome_arquivo}"
        texto_final = f"# {titulo}\n\n{conteudo}"
        
        with console.status("[bold cyan]Sincronizando textos...[/bold cyan]"):
            sucesso = enviar_para_github(caminho_md, texto_final, f"Adicionando página: {titulo}")
            
        if sucesso:
            console.print(f"\n[bold green]✅ Página publicada![/bold green] O GitBook irá renderizar [cyan]{caminho_md}[/cyan] em instantes.\n")

def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel.fit("[bold magenta]Forja de Conteúdo RPG (Cloud)[/bold magenta]\n[dim]Integração Direta: GitHub Sync -> GitBook[/dim]", border_style="magenta"))
        
        while True:
            acao = questionary.select(
                "O que você deseja transmitir para a nuvem?",
                choices=[
                    questionary.Choice("📝 Escrever Nova Página / Regra", value="1"),
                    questionary.Choice("🐉 Forjar Inimigo (Bestiário + VTT)", value="2"),
                    questionary.Choice("❌ Sair", value="3")
                ],
                pointer="👉"
            ).ask()
            
            if acao == "1":
                modulo_escrita_livre()
            elif acao == "2":
                modulo_criador_bestiario()
            elif acao == "3" or acao is None:
                console.print("[yellow]Desconectando do servidor...[/yellow]")
                break
                
    except KeyboardInterrupt:
        console.print("\n\n[bold yellow]⚠️ Operação cancelada de emergência.[/bold yellow]")

if __name__ == "__main__":
    main()