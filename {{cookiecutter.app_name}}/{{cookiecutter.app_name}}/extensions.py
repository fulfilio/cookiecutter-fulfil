# -*- coding: utf-8 -*-
import os

import flask
from flask_babel import Babel
from flask_debugtoolbar import DebugToolbarExtension
from celery import Celery
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from fulfil_client.oauth import Session
from fulfil_client import Client, BearerAuth, ClientError
from werkzeug.local import LocalProxy
from raven.contrib.flask import Sentry

# Setup fulfil session
Session.setup(
    os.environ['FULFIL_APP_ID'], os.environ['FULFIL_APP_SECRET']
)

try:
    from raven import Client as SentryClient
    from raven.contrib.celery import register_signal
except ImportError:
    pass
else:
    if os.environ.get('SENTRY_DSN'):
        sentry_client = SentryClient(os.environ.get('SENTRY_DSN'))
        register_signal(sentry_client)


celery = Celery('{{cookiecutter.app_name}}')
redis_store = FlaskRedis()
babel = Babel()
toolbar = DebugToolbarExtension()
sentry = Sentry()


def make_celery(app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                if '_subdomain' in kwargs:
                    flask.g._fulfil = Client(
                        kwargs['_subdomain'],
                        auth=BearerAuth(
                            kwargs['_access_token']
                        )

                    )
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


# Database
db = SQLAlchemy()
migrate = Migrate()


def get_fulfil():
    # Check if set on global. This happens from
    # celery tasks
    fulfil = getattr(flask.g, '_fulfil', None)
    if fulfil is not None:
        return fulfil

    if 'fulfil' not in flask.session:
        return

    session_data = flask.session['fulfil']
    try:
        return Client(
            flask.session['subdomain'],
            auth=BearerAuth(
                session_data['oauth_token']['access_token']
            )
        )
    except ClientError as e:
        if e.code == 401:
            # unauthorized
            # TODO: Use refresh token if possible
            flask.abort(flask.redirect(flask.url_for('user.logout')))
        raise


fulfil = LocalProxy(get_fulfil)


def get_oauth_user():
    from user.models import User

    if 'fulfil' not in flask.session:
        return User()
    session_data = flask.session['fulfil']
    oauth_user = User(
        session_data['user']['id'],
        session_data['user']['name'],
        session_data['user']['email'],
        subdomain=flask.session['subdomain'],
    )
    return oauth_user


oauth_user = LocalProxy(get_oauth_user)


def encr_key():
    """Returns encription key from app config
    """
    return flask.current_app.config['ENCR_KEY']
