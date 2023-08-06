
import os
import click


TEMPLATE_URL = 'https://github.com/connormullett/FlaskBoilerPlate.git'


@click.group()
def main():
    pass

@main.command()
def start():

    project_name = click.prompt('Enter project name')

    path = os.getcwd()
    if click.confirm('User Authentication?'):
        os.system('git clone %s %s/%s' % (TEMPLATE_URL, path, project_name))

    else:
        os.system('git clone %s --branch no-auth %s/%s' % (TEMPLATE_URL, path, project_name))

