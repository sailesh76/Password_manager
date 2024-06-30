import mysql.connector


from rich import print as printc
from rich.console import Console
console = Console()

def dbconfig():
    try:
        db = mysql.connector.connect(  # Fix: mysql.connector instead of mysql.connecter
            host='localhost',
            user='pm',
            password='password'  # Fix: password instead of passwd
        )
        return db  # Move the return statement inside the function

    except Exception as e:
        console.print_exception(show_locals=True)
        return None  # Return None in case of an exception