import click
from flask import current_app
from flask.cli import with_appcontext


@click.group()
def cli():
    pass


@cli.command()
@with_appcontext
def delete_expired():
    ''' Deletes expired uploads '''
    click.echo('Deleting expired uploads')
    try:
        current_app.flask_tus.repo.delete_expired()
    except Exception as e:
        click.echo(e)
    else:
        click.echo('Successfully deleted expired uploads deleted')
