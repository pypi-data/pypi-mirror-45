from consul import Consul
from black_holes.core import BlackHole
from black_holes.models import Secret, db
from peewee import DoesNotExist, OperationalError


class DatabaseBlackHole(BlackHole):
    """Secrets administration based on a Sqlite database."""

    def init_motor(self):
        """Development Wormhole Initialization"""

        try:
            # Init DB Connection
            db.connect()
            # Migrate
            db.create_tables([Secret])
        except OperationalError as oe:
            if not str(oe) == 'Connection already opened.':
                raise oe

    def set(self, key, value):
        """Update or Create Key on sqlite.database."""

        try:
            self.update(key, value)
        except DoesNotExist:
            Secret.create(key=key, value=value)

    @staticmethod
    def update(key, value):
        """Update Key on sqlite.database."""
        s = Secret.get(key=key)
        s.value = value
        s.save()

    def delete(self, key):
        """Drop Key from sqlite.database by Key"""
        try:
            s = Secret.get(key=key)
            s.delete_instance()
        except DoesNotExist:
            return

    def get(self, key):
        """Retrieve Value from sqlite.database by Key."""
        try:
            return Secret.get(key=key).value
        except DoesNotExist:
            return

    def fetch(self):
        """List Database secrets"""

        raw = Secret.select()
        secrets = []
        for _secret in raw:
            secrets.append({'key': _secret.key, 'value': _secret.value})
        return secrets


class RemoteWormhole(BlackHole):

    consul = Consul()

    def __init__(self, token=None, **kwargs):
        """Remote Wormhole Initialization"""

        super().__init__(**kwargs)
        if token is not None:
            self.consul = None
            self.consul = Consul(token=token)

    def set(self, key, value):
        """Store Key and Value in Consul."""
        self.consul.kv.put(key, value)

    def get(self, key):
        """Retrieve Value from Consul by Key."""

        idx, data = self.consul.kv.get(key)
        try:
            value = data['Value']
        except TypeError:
            value = None
        if isinstance(value, bytes):
            value = value.decode()
        return value

    def delete(self, key):
        """Remove Key from Consul by Key."""
        self.consul.kv.delete(key)

    def fetch(self):
        """List all Consul keys is not allowed."""
        raise AttributeError('Method Not Allowed')
