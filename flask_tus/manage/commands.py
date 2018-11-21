import click
from flask import current_app
from flask.cli import with_appcontext


@click.group()
def cli():
    pass


@cli.command()
@with_appcontext
def delete_expired():
    click.echo('Deleting expired uploads')
    try:
        current_app.flask_tus.model.delete_expired()
    except Exception as e:
        click.echo(e)
    else:
        click.echo('Succesfully deleted expired uploads deleted')
