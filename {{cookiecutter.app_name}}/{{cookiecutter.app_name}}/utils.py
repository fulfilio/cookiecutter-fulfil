# -*- coding: utf-8 -*-
import json
from functools import wraps, partial

import jwt
from flask import abort, url_for, redirect, request, session
from fulfil_client.oauth import Session
from fulfil_client.serialization import JSONEncoder, JSONDecoder

dumps = partial(json.dumps, cls=JSONEncoder)
loads = partial(json.loads, object_hook=JSONDecoder())


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('fulfil') is None:
            if request.is_json:
                abort(401)
            return redirect(
                url_for('user.login', next=request.url)
            )
        return f(*args, **kwargs)
    return decorated_function


def decode_jwt(token):
    try:
        return jwt.decode(token, verify=False)
    except jwt.exceptions.InvalidTokenError:
        return


def get_oauth_session(scope=None):
    if 'subdomain' in session:
        return Session(session['subdomain'])
    raise Exception("'subdomain' should be in session.")
