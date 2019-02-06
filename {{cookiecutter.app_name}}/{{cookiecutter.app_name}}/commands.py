import click
from flask.cli import AppGroup

maint_cli = AppGroup('maint')


@maint_cli.command('clear_migration_history')
def clear_migration_history():
    """Clear migration history"""
    from {{cookiecutter.app_name}}.extensions import db

    db.engine.execute("drop table if exists alembic_version;")
    print("Dropped alembic_version table")
