from sys import exit
import yaml
import click
from os.path import expanduser

STORE_FILE = expanduser("~") + '/.deutscher-befrager-store'

def load_store():
    try:
        store_file = open(STORE_FILE,"r+") 
        raw_content = store_file.read()
        store_file.seek(0)
        content = _parse_raw_store(raw_content)
        return content
    except FileNotFoundError:
        click.echo(f"You don't have a {STORE_FILE} yet")
        _create_store()

def _parse_raw_store(raw_txt):
    try:
        return yaml.load(raw_txt, Loader=yaml.FullLoader)
    except yaml.YAMLError as ymlexcp:
        click.echo(f"Error parcing your {STORE_FILE}")
        click.echo(ymlexcp)

def _create_store():
    """Create a store file to house the users questions, answers, and grade values"""
    should_create_file = input("Would you like me to create one y/n?")
    click.echo("Ok making new store file")
    if should_create_file == 'y':
        try:
            store_file = open(STORE_FILE,"w") 
            store_file.write("")
            store_file.close()
            click.echo(f"Created blank store file {STORE_FILE}.")
        except:
            click.echo("Problem creating store file :'(")
        click.echo("Time to ask some questions!")
    exit(0)


def save_store(val):
    """Save yaml to the users store file"""
    store_file = open(STORE_FILE,"w") 
    store_string = yaml.dump(val)
    store_file.write(store_string)
    store_file.truncate()
    store_file.close()
