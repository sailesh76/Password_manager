from getpass import getpass
from utils.dbconfig import dbconfig
import hashlib
import string
import random
import sys

from rich import print as printc
from rich.console import Console

console = Console()


def generatedevicesecret(length=10):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def config():
    # Create A Database
    db = dbconfig()
    if db is None:
        printc("[red][!] Unable to connect to the database.[/red]")
        sys.exit(0)

    cursor = db.cursor()
    
    printc("[green][+] Creating new config [/green]")
    
    try:
        cursor.execute("CREATE DATABASE pm")
    except Exception as e:
        printc("[red][!] An error occurred while trying to create database.")
        console.print_exception(show_locals=True)
        sys.exit(0)
    printc("[green][+][/green] Database 'pm' created")

    # create tables
    query = "CREATE TABLE pm.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    cursor.execute(query)
    printc("[green][+][/green] Table 'secrets' created")

    query = "CREATE TABLE pm.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password  TEXT NOT NULL)"
    cursor.execute(query)
    printc("[green][+][/green] Table 'entries' created")

    mp = ""
    while True:
        mp = getpass("Choose your Master Password:")
        if mp == getpass("re-type: ") and mp != "":
            printc("[yellow][-] Please try again.[/yellow]")
        else:
            break

    # HASH THE MASTER PASSWORD
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    printc("[green][+][/green] GENERATED HASH OF MASTER PASSWORD")

    # GENERATE A DEVICE SECRET
    ds = generatedevicesecret()
    printc("[green][+][/green] Device secret generated")

    # add them to database
    query = "INSERT INTO pm.secrets (masterkey_hash, device_secret) values(%s,%s)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()

    printc("[green][+][/green] Added to the database")

    printc("[green][+] Configuration done![/green]")

    db.close()


config()