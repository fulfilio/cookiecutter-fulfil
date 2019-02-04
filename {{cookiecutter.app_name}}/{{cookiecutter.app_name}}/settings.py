# -*- coding: utf-8 -*-
"""Application configuration."""
import os

from flask.helpers import get_debug_flag


class Config(object):
    """Base configuration."""

    if not get_debug_flag():
        # Assert env for prod
        keys = (
            'ENCR_KEY', '{{ cookiecutter.app_name|upper }}_SECRET_KEY',
            'DATABASE_URI'
        )
        for key in keys:
            assert key in os.environ, \
                f'Environment variable "{key}" is missing.'

    SECRET_KEY = os.environ['{{ cookiecutter.app_name|upper }}_SECRET_KEY']
    ENCR_KEY = os.environ.get('ENCR_KEY', 'encr-key')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

    # Example ['sale.channel:read', 'sale.channel:write']
    FULFIL_PERMISSIONS = ['party.party:read']


class ProdConfig(Config):
    pass


class DevConfig(Config):
    pass
