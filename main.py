import os
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def banner():
    ascii_art = """
     ██████╗██╗██╗     ███████╗███╗   ██╗████████╗███████╗
    ██╔════╝██║██║     ██╔════╝████╗  ██║╚══██╔══╝╚══███╔╝
    ╚█████╗ ██║██║     █████╗  ██╔██╗ ██║   ██║     ███╔╝ 
     ╚═══██╗██║██║     ██╔══╝  ██║╚██╗██║   ██║    ███╔╝  
    ██████╔╝██║███████╗███████╗██║ ╚████║   ██║   ███████╗
    ╚═════╝ ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝
                [ LINUX PRIVILEGE ESC ]
    """
    console.print(Panel(ascii_art, style="bold magenta", expand=False))

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip()
    except:
        return "Erreur ou accès refusé"

def check_system():
    table = Table(title="Informations Systeme")
    table.add_column("Cible", style="cyan")
    table.add_column("Valeur", style="white")
    
    table.add_row("Kernel", run_cmd("uname -a"))
    table.add_row("Hostname", run_cmd("hostname"))
    table.add_row("Utilisateur", run_cmd("whoami"))
    table.add_row("ID", run_cmd("id"))
    
    console.print(table)

def check_suid():
    console.print("\n[bold yellow][!] Recherche de fichiers SUID (Vecteurs potentiels)...[/bold yellow]")
    suid_files = run_cmd("find / -perm -u=s -type f 2>/dev/null | head -n 15")
    if suid_files:
        console.print(Panel(suid_files, title="Top 15 SUID", style="red"))
    else:
        console.print("[green]Aucun SUID inhabituel trouvé.[/green]")

def check_writable():
    console.print("\n[bold yellow][!] Dossiers ouverts en ecriture...[/bold yellow]")
    writable = run_cmd("find / -writable -type d 2>/dev/null | cut -d'/' -f1-3 | sort | uniq | head -n 10")
    console.print(Panel(writable, title="Dossiers Writable", style="blue"))

def check_sensitive_files():
    files = ["/etc/passwd", "/etc/shadow", "/root/.ssh/id_rsa", "/home/*/.ssh/id_rsa", "/var/www/html/config.php"]
    table = Table(title="Acces aux fichiers sensibles")
    table.add_column("Fichier", style="cyan")
    table.add_column("Permission", style="bold")

    for f in files:
        if os.access(f, os.R_OK):
            table.add_row(f, "[red]LISIBLE[/red]")
        else:
            table.add_row(f, "[green]PROTEGE[/green]")
    
    console.print(table)

def main():
    os.system('clear')
    banner()
    
    check_system()
    check_suid()
    check_writable()
    check_sensitive_files()
    
    console.print("\n[bold white]Analyse post-exploitation terminee.[/bold white]")

if __name__ == "__main__":
    main()
