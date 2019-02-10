import json
from werkzeug.utils import cached_property

from flask import abort
from fulfil_client import Client, BearerAuth
from sqlalchemy_utils import EncryptedType

from ..database import Column, Model, db, SurrogatePK
from ..extensions import encr_key, redis_store


class Merchant(SurrogatePK, Model):
    __tablename__ = 'merchant'

    name = Column(db.String(80), nullable=False)
    company_fid = Column(db.Integer, nullable=False)
    subdomain = Column(db.String(80), nullable=False, unique=True)
    timezone = Column(db.String(80), nullable=False, unique=True)
    token = Column(EncryptedType(db.String, encr_key), nullable=False)

    @cached_property
    def fulfil_client(self):
        key = 'fulfil:user:%s:context' % self.token
        context = redis_store.get(key)
        if context:
            client = Client(
                self.subdomain, auth=BearerAuth(self.token),
                context=json.loads(context)
            )
        else:
            client = Client(self.subdomain, auth=BearerAuth(self.token))
            redis_store.set(key, json.dumps(client.context), 300)  # TTL 5min
        return client

    @classmethod
    def get_by_subdomain(cls, name):
        """Find merchant by subdomain
        """
        return cls.query.filter_by(subdomain=name).first()

    @classmethod
    def get_or_404(cls, subdomain):
        merchant = cls.get_by_subdomain(subdomain)
        if not merchant:
            abort(404)
        return merchant

    @classmethod
    def create_or_update(cls, subdomain, token, name):
        merchant = cls.get_by_subdomain(subdomain)
        if not merchant:
            merchant = cls()
        merchant.name = name
        merchant.subdomain = subdomain
        merchant.token = token
        merchant.save()
        return merchant


class User:
    def __init__(self, id=None, name=None, email=None, **kwargs):
        self.id = id
        self.name = name
        self.email = email
        self.subdomain = kwargs.get('subdomain')

    @cached_property
    def is_support(self):
        return self.email and self.email.endswith('@fulfil.io')

    @cached_property
    def is_anonymous(self):
        return self.id

    @cached_property
    def merchant(self):
        return Merchant.get_by_subdomain(self.subdomain)

    @cached_property
    def serialize(self):
        return {
            'name': self.name,
            'email': self.email,
            'id': self.id,
            'subdomain': self.subdomain
        }
