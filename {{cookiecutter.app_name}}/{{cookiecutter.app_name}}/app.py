# -*- coding: utf-8 -*-
from flask import Flask
from flask_sslify import SSLify
from werkzeug.contrib.fixers import ProxyFix

from .extensions import (
    babel, toolbar, sentry, oauth_user, db, migrate, redis_store, csrf_protect
{% if cookiecutter.use_async_task == "yes" %}    setup_dramatiq{% endif %}
)
from .globals import register_globals
from .settings import Config

{% if cookiecutter.use_async_task == "yes" %}
setup_dramatiq()
# Jobs are added here as dramatiq requires broker initialization
from {{cookiecutter.app_name}}.jobs import * # noqa
{% endif %}

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Behind ELB
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # register extensions
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)
    csrf_protect.init_app(app)
    toolbar.init_app(app)
    sentry.init_app(app)
    redis_store.init_app(app)

    if not app.debug:
        SSLify(app)

    register_context_processors(app)
    register_globals(app)
    register_cmd(app)
    register_shell_context_processor(app)

    # register blueprints
    from {{cookiecutter.app_name}}.user.views import blueprint
    app.register_blueprint(blueprint)

    return app


def register_context_processors(app):
    app.context_processor(lambda: {
        'oauth_user': oauth_user,
    })


def register_cmd(app):
    from {{cookiecutter.app_name}} import commands

    app.cli.add_command(commands.maint_cli)


def register_shell_context_processor(app):
    from {{cookiecutter.app_name}}.user.models import Merchant

    app.shell_context_processor(lambda: {
        'Merchant': Merchant,
    })
