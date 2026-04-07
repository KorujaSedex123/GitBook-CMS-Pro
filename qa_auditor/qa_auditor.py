import os
import re
import csv
import time
import requests
import questionary
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()

def get_headers():
    load_dotenv()
    token = os.getenv("GITBOOK_TOKEN")
    if not token:
        console.print("[red]❌ Token não encontrado no .env![/red]")
        exit()
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def fetch_com_resiliencia(url, headers):
    for _ in range(4):
        res = requests.get(url, headers=headers)
        if res.status_code == 429:
            time.sleep(int(res.headers.get('Retry-After', 3)))
            continue
        return res
    return None

def buscar_arvore_recursiva(pages):
    lista_final = []
    for p in pages:
        lista_final.append({"id": p.get("id"), "title": p.get("title")})
        if 'pages' in p:
            lista_final.extend(buscar_arvore_recursiva(p['pages']))
    return lista_final

def auditar_pagina(titulo, markdown_puro):
    alertas = []
    status = {"Nome": titulo, "PV": "-", "Defesa": "-", "Dano": "-", "Arte": "Sim"}

    if not markdown_puro or len(markdown_puro.strip()) < 15:
        alertas.append("Página vazia ou incompleta")
        status["Arte"] = "Não"
        return status, alertas

    # 1. Checagem de QA (Qualidade)
    if not re.search(r'!\[.*?\]\(.*?\)', markdown_puro) and not '<img' in markdown_puro:
        alertas.append("Sem imagem/arte")
        status["Arte"] = "Não"
        
    if "todo" in markdown_puro.lower() or "wip" in markdown_puro.lower():
        alertas.append("Marcação TODO/WIP encontrada")

    # 2. Extração de Balanceamento (Procura por números de PV, Defesa e Dano)
    # Busca variações como "PV:", "PV (Saúde):", "Defesa:", "Armadura:", etc.
    pv_match = re.search(r'(?:PV|Saúde).*?(\d+)', markdown_puro, re.IGNORECASE)
    if pv_match: status["PV"] = int(pv_match.group(1))

    def_match = re.search(r'(?:Defesa|Armadura).*?(\d+)', markdown_puro, re.IGNORECASE)
    if def_match: status["Defesa"] = int(def_match.group(1))

    dano_match = re.search(r'(?:Dano).*?(\d+|[0-9]+[dD][0-9]+(?:\+[0-9]+)?)', markdown_puro, re.IGNORECASE)
    if dano_match: status["Dano"] = dano_match.group(1)
    
    # Se achou PV, mas esqueceu a defesa ou dano, gera um alerta
    if status["PV"] != "-" and (status["Defesa"] == "-" or status["Dano"] == "-"):
        alertas.append("Status de combate incompletos")

    return status, alertas

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel.fit("[bold magenta]GitBook QA & Balance Auditor[/bold magenta]\n[dim]Inspeção de Integridade e Extração de Métricas[/dim]", border_style="magenta"))
    
    headers = get_headers()
    
    with console.status("[bold green]Acessando banco de dados da API...[/bold green]"):
        r_orgs = fetch_com_resiliencia("https://api.gitbook.com/v1/orgs", headers)
        espacos = []
        if r_orgs and r_orgs.status_code == 200:
            for org in r_orgs.json().get('items', []):
                r_spaces = fetch_com_resiliencia(f"https://api.gitbook.com/v1/orgs/{org['id']}/spaces", headers)
                if r_spaces and r_spaces.status_code == 200:
                    for sp in r_spaces.json().get('items', []):
                        sp['org_name'] = org.get('title', 'Sua Organização')
                        espacos.append(sp)
                        
    if not espacos:
        return console.print("[red]❌ Nenhum projeto encontrado.[/red]")
        
    opcoes = [questionary.Choice(f"📚 {sp.get('title')} (Org: {sp.get('org_name')})", value=sp) for sp in espacos]
    opcoes.append(questionary.Choice("❌ Sair", value=None))

    espaco_escolhido = questionary.select(
        "Selecione o manual para realizar a auditoria:",
        choices=opcoes,
        pointer="👉"
    ).ask()
    
    if not espaco_escolhido: return
    
    SPACE_ID = espaco_escolhido['id']
    
    # Mapeando todas as páginas
    r_paginas = fetch_com_resiliencia(f"https://api.gitbook.com/v1/spaces/{SPACE_ID}/content", headers)
    paginas_lista = buscar_arvore_recursiva(r_paginas.json().get('pages', []))
    
    resultados_balanceamento = []
    relatorio_qa = []
    
    # Varredura
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), console=console) as progress:
        task = progress.add_task("[cyan]Auditando páginas...", total=len(paginas_lista))
        
        for p in paginas_lista:
            progress.update(task, description=f"[cyan]Auditando: {p['title'][:20]}...")
            
            res = fetch_com_resiliencia(f"https://api.gitbook.com/v1/spaces/{SPACE_ID}/content/page/{p['id']}?format=markdown", headers)
            md_puro = res.json().get("markdown", "") if res and res.status_code == 200 else ""
            
            status, alertas = auditar_pagina(p['title'], md_puro)
            
            if alertas:
                relatorio_qa.append({"titulo": p['title'], "alertas": alertas})
                
            # Se a página tiver estatísticas de combate (identificado por ter PV), salva pro CSV
            if status["PV"] != "-":
                resultados_balanceamento.append(status)
                
            progress.advance(task)

    # ---------------------------------------------------------
    # EXIBIÇÃO DOS RESULTADOS (QA)
    # ---------------------------------------------------------
    console.print("\n")
    if relatorio_qa:
        tabela_qa = Table(title="⚠️ RELATÓRIO DE QUALIDADE (Páginas com problemas)", show_header=True, header_style="bold red")
        tabela_qa.add_column("Página", style="bold white", width=30)
        tabela_qa.add_column("Alertas Encontrados", style="yellow")
        
        for item in relatorio_qa:
            tabela_qa.add_row(item['titulo'], "\n".join(item['alertas']))
            
        console.print(tabela_qa)
    else:
        console.print("[bold green]✅ Auditoria de Qualidade Perfeita![/bold green] Nenhuma página vazia ou sem imagem encontrada.")

    # ---------------------------------------------------------
    # EXPORTAÇÃO E EXIBIÇÃO DE BALANCEAMENTO (MÉTRICAS)
    # ---------------------------------------------------------
    if resultados_balanceamento:
        tabela_bal = Table(title="📊 MÉTRICAS DE COMBATE (Bestiário Extraído)", show_header=True, header_style="bold cyan")
        tabela_bal.add_column("Ameaça / Monstro", style="bold white")
        tabela_bal.add_column("PV", justify="center", style="green")
        tabela_bal.add_column("Defesa", justify="center", style="blue")
        tabela_bal.add_column("Dano Base", justify="center", style="red")
        
        for b in resultados_balanceamento:
            tabela_bal.add_row(b["Nome"], str(b["PV"]), str(b["Defesa"]), str(b["Dano"]))
            
        console.print("\n")
        console.print(tabela_bal)
        
        # Exportar CSV
        arquivo_csv = "planilha_de_balanceamento.csv"
        with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Nome", "PV", "Defesa", "Dano", "Arte"])
            writer.writeheader()
            for row in resultados_balanceamento:
                writer.writerow(row)
                
        console.print(f"\n[bold green]💾 Planilha salva![/bold green] Abra o arquivo [cyan]{arquivo_csv}[/cyan] no Excel para criar gráficos e comparar o nível de poder das suas ameaças.")

if __name__ == "__main__":
    main()