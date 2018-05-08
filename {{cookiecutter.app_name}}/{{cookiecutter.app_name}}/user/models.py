import json
from werkzeug.utils import cached_property

from flask import abort
from fulfil_client import Client, BearerAuth
from sqlalchemy_utils import EncryptedType

from ..database import Column, Model, db, SurrogatePK
from ..extensions import encr_key, redis_store


class Organization(SurrogatePK, Model):
    __tablename__ = 'organization'

    name = Column(db.String(80), nullable=False)
    subdomain = Column(db.String(80), nullable=False, unique=True)
    token = Column(EncryptedType(db.String, encr_key), nullable=False)

    @cached_property
    def fulfil_client(self):
        key = 'fulfil:user:%s:context' % self.token
        context = redis_store.get(key)
        if context:
            client = Client(self.subdomain, auth=BearerAuth(self.token),
                            context=json.loads(context))
        else:
            client = Client(self.subdomain, auth=BearerAuth(self.token))
            redis_store.set(key, json.dumps(client.context), 300)  # TTL 5min
        return client

    @classmethod
    def get_by_subdomain(cls, name):
        """Find qrganization by subdomain
        """
        return cls.query.filter_by(subdomain=name).first()

    @classmethod
    def get_or_404(cls, subdomain):
        organization = cls.get_by_subdomain(subdomain)
        if not organization:
            abort(404)
        return organization

    @classmethod
    def create_or_update(cls, subdomain, token, name):
        organization = cls.get_by_subdomain(subdomain)
        if not organization:
            organization = cls()
        organization.name = name
        organization.subdomain = subdomain
        organization.token = token
        organization.save()
        return organization


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
    def organization(self):
        return Organization.get_by_subdomain(self.subdomain)
