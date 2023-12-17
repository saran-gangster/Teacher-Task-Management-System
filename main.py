# SCHOOL MANAGEMENT SYSTEM...

# Importing
from typing import Final
from time import sleep
from sys import exit
import mysql.connector as msc
import src
from dotenv import load_dotenv,find_dotenv
from os import getenv
from getpass import getpass
from rich.console import Console
from rich import print as rprint
from rich.table import Table

load_dotenv(find_dotenv())
console = Console()

# Declaring ENV Variables 

MYSQL_HOST: Final = getenv('MYSQL_HOST')
MYSQL_PORT: Final = getenv('MYSQL_PORT')
MYSQL_USER: Final = getenv('MYSQL_USER')
MYSQL_PASSWORD: Final = getenv('MYSQL_PASSWORD')
MYSQL_DATABASE: str = getenv('MYSQL_DATABASE')

rprint(r'''
[green]
d888888b d88888b  .d8b.   .o88b. db   db d88888b d8888b.      d888888b  .d8b.  .d8888. db   dD      .88b  d88.  .d8b.  d8b   db  .d8b.   d888b  d88888b .88b  d88. d88888b d8b   db d888888b      .d8888. db    db .d8888. d888888b d88888b .88b  d88. 
`~~88~~' 88'     d8' `8b d8P  Y8 88   88 88'     88  `8D      `~~88~~' d8' `8b 88'  YP 88 ,8P'      88'YbdP`88 d8' `8b 888o  88 d8' `8b 88' Y8b 88'     88'YbdP`88 88'     888o  88 `~~88~~'      88'  YP `8b  d8' 88'  YP `~~88~~' 88'     88'YbdP`88 
   88    88ooooo 88ooo88 8P      88ooo88 88ooooo 88oobY'         88    88ooo88 `8bo.   88,8P        88  88  88 88ooo88 88V8o 88 88ooo88 88      88ooooo 88  88  88 88ooooo 88V8o 88    88         `8bo.    `8bd8'  `8bo.      88    88ooooo 88  88  88 
   88    88~~~~~ 88~~~88 8b      88~~~88 88~~~~~ 88`8b           88    88~~~88   `Y8b. 88`8b        88  88  88 88~~~88 88 V8o88 88~~~88 88  ooo 88~~~~~ 88  88  88 88~~~~~ 88 V8o88    88           `Y8b.    88      `Y8b.    88    88~~~~~ 88  88  88 
   88    88.     88   88 Y8b  d8 88   88 88.     88 `88.         88    88   88 db   8D 88 `88.      88  88  88 88   88 88  V888 88   88 88. ~8~ 88.     88  88  88 88.     88  V888    88         db   8D    88    db   8D    88    88.     88  88  88 
   YP    Y88888P YP   YP  `Y88P' YP   YP Y88888P 88   YD         YP    YP   YP `8888Y' YP   YD      YP  YP  YP YP   YP VP   V8P YP   YP  Y888P  Y88888P YP  YP  YP Y88888P VP   V8P    YP         `8888Y'    YP    `8888Y'    YP    Y88888P YP  YP  YP 

[/green][bold blue]
By Saran
[/ bold blue]
''')





def main():

    rprint("Enter the password")
    inputPassword: str = getpass(':')

    src.Enter()

    with console.status("[bold green]Verifying Password..") as status:
        sleep(3)
        if inputPassword != MYSQL_PASSWORD:
            console.log("[bold red]ACCESS DENIED![/bold red]")
            exit()
        else:
            console.log("[green]Password Verified![/green]")

    with console.status("[bold green]Checking for MYSQL Connection..") as status:
        sleep(3)
        try:
            connection = msc.connect(host = MYSQL_HOST , port = MYSQL_PORT , user = MYSQL_USER , passwd = MYSQL_PASSWORD)
            cursor = connection.cursor()
            if connection.is_connected():
                console.log(f"[green]Connection Established ![/green]")
        except:
            console.log(f'[bold][red]Unable to Connect to MYSQL Server ')
            exit()

    
    with console.status("[bold green]Checking for Database..") as status:
        sleep(2)
        if MYSQL_DATABASE == '':
            console.log(f'[bold][red]Database Not Defined. ')
            database = False
        else:
            database = MYSQL_DATABASE
            console.log(f'[bold][green]Database Found. ')
   
    if not database:
        database  = src.create_database(cursor,console)
    connection = msc.connect(host = MYSQL_HOST , port = MYSQL_PORT , user = MYSQL_USER , passwd = MYSQL_PASSWORD , database = database)
    cursor = connection.cursor()
    src.create_table(cursor,console)

    while True:
        src.Enter()
        table = Table(title="Akkupy School")
        table.add_column("S. No.", style="cyan", no_wrap=True)
        table.add_column("Section", style="magenta")
        table.add_row("1","Students")
        table.add_row("2","Teachers")
        table.add_row("3","Classes")
        table.add_row("4","Exit")
        console.print(table)
        sectionValue = src.Choice("Enter a Choice(1,2,3,4)", [1, 2, 3, 4])

        match sectionValue:
            case 1:
                src.Student(cursor,connection,console)
            case 2:
                src.Teachers(cursor,connection)
            case 3:
                src.Class(cursor,connection)
            case 4:
                with console.status("[red bold]Quitting Program....[/red bold]") as status:
                    sleep(3)
                    connection.close()
                    console.log("[bold red] Bye.[/bold red]")
                    exit()


    
if __name__=="__main__":
    main()
