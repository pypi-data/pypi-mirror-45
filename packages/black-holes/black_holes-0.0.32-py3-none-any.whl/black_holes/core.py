import json
import base64
import logging
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


logger = logging.getLogger(__name__)


class BlackHoleBase:

    __secrets__: dict = {}

    def __init__(self, **kwargs):
        self.init_motor()
        self.bulk(keys_bulk=kwargs)

    def before_init_motor(self, **kwargs) -> None: ...

    def init_motor(self) -> None: ...

    def before_get_attr(self, key) -> str:
        return key

    def before_set_attr(self, key, value) -> tuple:
        return key, value

    def after_get_attr(self, key, value) -> any:
        return key, value

    def get(self, key):
        return self.__secrets__.get(key)

    def set(self, key, value):
        self.__secrets__.update({key: value})

    def delete(self, key):
        del self.__secrets__[key]

    def fetch(self):
        return [k for k in self.__secrets__.keys()]

    def __setter__(self, key, value):
        key, value = self.before_set_attr(key=key, value=value)
        self.set(key=key, value=value)

    def __getter__(self, key):
        key_filtered = self.before_get_attr(key=key)
        value = self.get(key_filtered)
        key, value = self.after_get_attr(key=key, value=value)
        return value

    def __getitem__(self, key):
        return self.__getter__(key=key)

    def __setitem__(self, key, value):
        self.__setter__(key=key, value=value)

    def __delitem__(self, key):
        self.delete(key=key)

    def __str__(self):
        return '%s' % json.dumps(self.__secrets__, indent=4)

    def __iter__(self):
        for _secret in self.fetch():
            yield {_secret.get('key'): _secret.get('value')}

    def bulk(self, keys_bulk):
        logger.debug('bulk upload')
        if not isinstance(keys_bulk, dict):
            raise TypeError
        for k, v in keys_bulk.items():
            self.__setter__(key=k, value=v)


class EnigmaMachineMixin:
    """Encrypt and Decrypt."""

    block_size = 16

    def pad(self, s):
        if isinstance(s, bytes):
            s = s.decode()
        res = s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)
        if isinstance(res, str):
            res = res.encode()
        return res

    @staticmethod
    def unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, message, password):
        """AES message argument encryption."""

        private_key = hashlib.sha256(password.encode("utf-8")).digest()
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        res = base64.b64encode(iv + cipher.encrypt(message))
        if isinstance(res, bytes):
            res = res.decode()
        return res

    def decrypt(self, encrypted_message, password):
        """AES encrypted message decryption."""
        try:
            private_key = hashlib.sha256(password.encode("utf-8")).digest()
            encrypted_message = base64.b64decode(encrypted_message)
            iv = encrypted_message[:16]
            cipher = AES.new(private_key, AES.MODE_CBC, iv)
            res = self.unpad(cipher.decrypt(encrypted_message[16:]))
            if isinstance(res, bytes):
                res = res.decode()
            return res
        except Exception as e:
            print(e)
            return


class BlackHole(BlackHoleBase, EnigmaMachineMixin):
    """Simple BlackHole with encryption layer"""

    def password(self) -> str:
        return 'qwerty1234567890'

    def before_set_attr(self, key, value) -> tuple:
        # Encrypt message
        if 'encrypted_' in key:
            value = self.encrypt(message=value, password=self.password())
            key = key.replace('encrypted_', '')
        return key, value

    def before_get_attr(self, key) -> str:
        return key.replace('decrypted_', '')

    def after_get_attr(self, key, value) -> tuple:
        if 'decrypted_' in key:
            value = self.decrypt(encrypted_message=value, password=self.password())
        return key, value

    def __init__(self, **kwargs):
        password_callback = kwargs.pop('password_callback', None)
        if callable(password_callback):
            self.password = password_callback
        BlackHoleBase.__init__(self, **kwargs)
