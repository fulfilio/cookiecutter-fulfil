# -*- coding: utf-8 -*-
import os

import flask
from flask_babel import Babel
from flask_debugtoolbar import DebugToolbarExtension
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from fulfil_client.oauth import Session
from fulfil_client import Client, BearerAuth, ClientError
from werkzeug.local import LocalProxy
from raven.contrib.flask import Sentry
{% if cookiecutter.use_async_task == "yes" %}
import dramatiq
from dramatiq.brokers.rabbitmq import URLRabbitmqBroker
from dramatiq.brokers.redis import RedisBroker
{% endif %}

# Setup fulfil session
Session.setup(
    os.environ['FULFIL_APP_ID'], os.environ['FULFIL_APP_SECRET']
)

redis_store = FlaskRedis()
babel = Babel()
toolbar = DebugToolbarExtension()
sentry = Sentry()

# Database
db = SQLAlchemy()
migrate = Migrate()


def get_fulfil():
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
    from {{cookiecutter.app_name}}.user.models import User

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
{% if cookiecutter.use_async_task == "yes" %}

def setup_dramatiq():
    if os.environ.get('AMQP_URL'):
        broker = URLRabbitmqBroker(os.environ['AMQP_URL'])
    else:
        broker = RedisBroker(url=os.environ['REDIS_URL'])
    dramatiq.set_broker(broker)
{% endif %}
