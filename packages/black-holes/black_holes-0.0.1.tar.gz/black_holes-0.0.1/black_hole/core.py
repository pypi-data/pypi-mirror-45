import base64
import hashlib
import logging
from Crypto import Random
from Crypto.Cipher import AES
from contextlib import suppress


logger = logging.getLogger(__name__)


class RedAlert(Exception):
    def __init__(self, message=''):
        if len(message) > 0:
            message = '. %s' % message
        super().__init__('Red Alert!' + message)


class BlackHoleBase:

    red_alert_key: str = 'red_alert'
    operative_value: str = 'operative'
    development: bool = True

    def __init__(self, **kwargs):
        self.development = kwargs.get('development', False)
        self.operative_value = kwargs.get('operative_value', 'operative_value')
        self.red_alert_key = kwargs.get('red_alert_key', 'red_alert')
        bulk_keys = kwargs.copy()
        # delete no longer required keys
        with suppress(KeyError):
            for k in ['development', 'red_alert_key', 'operative_value']:
                del bulk_keys[k]
        # Initialize key storage motor
        self.init_motor()
        # Set alert Key/Value (development mode)
        if self.development:
            self.add(self.red_alert_key, self.operative_value)
        # load bulk keys
        self.bulk(bulk_keys)

    def before_perform_get(self, key) -> str:
        """Task performed before get element."""

    def after_perform_get(self, key, value) -> tuple:
        """Task performed after get value"""
        return key, value

    def before_perform_set(self, key, value) -> tuple:
        """Task performed before set element."""

    def after_perform_set(self, key, value) -> tuple:
        """Task performed after set value"""

    def init_motor(self):
        """Initialize Key/Value storage motor"""

    def add(self, key, value):
        raise KeyError

    def delete(self, key):
        raise KeyError

    def get(self, key) -> any:
        raise KeyError

    def update(self, key, value):
        raise KeyError

    def fetch(self) -> list:
        raise IOError

    def alert(self, *args, **kwargs):
        """Alert Definition"""
        raise RedAlert('We are under attack.')

    def check_alerts(self):
        """Red Alert trigger."""
        status = self.get(self.red_alert_key)
        if not status == self.operative_value:
            self.alert()

    def __setter__(self, key, value):
        logger.debug('>> SET: key=%s' % key)
        self.check_alerts()
        key, value = self.before_perform_set(key=key, value=value)
        self.add(key=key, value=value)
        self.after_perform_set(key=key, value=value)

    def __getter__(self, key):
        logger.debug('<< GET: key=%s' % key)
        self.check_alerts()
        _key = self.before_perform_get(key)
        _value = self.get(_key)
        _key, _value = self.after_perform_get(key=key, value=_value)
        return _value

    def __deleter__(self, key):
        logger.debug('** DEL: key=%s' % key)
        self.check_alerts()
        self.delete(key=key)

    def __setattr__(self, key, value):
        self.__setter__(key=key, value=value)

    def __setitem__(self, key, value):
        self.__setter__(key=key, value=value)

    def __getitem__(self, item):
        return self.__getter__(key=item)

    def __getattr__(self, key):
        return self.__getter__(key=key)

    def __delattr__(self, key):
        self.__deleter__(key=key)

    def __delitem__(self, key):
        self.__deleter__(key=key)

    def bulk(self, keys_bulk):
        logger.debug('bulk upload')
        if not isinstance(keys_bulk, dict):
            raise TypeError
        for k, v in keys_bulk.items():
            self.add(key=k, value=v)

    def __iter__(self):
        self.check_alerts()
        for _secret in self.fetch():
            # self.check_alerts()
            yield {_secret.get('key'): _secret.get('value')}


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
        private_key = hashlib.sha256(password.encode("utf-8")).digest()
        encrypted_message = base64.b64decode(encrypted_message)
        iv = encrypted_message[:16]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        res = self.unpad(cipher.decrypt(encrypted_message[16:]))
        if isinstance(res, bytes):
            res = res.decode()
        return res


class BlackHole(BlackHoleBase, EnigmaMachineMixin):
    """BlackHoles with AES encryption capability."""

    def get_password(self):
        """Recovery password from db"""
        try:
            password = self.get('encryption_password')
        except IndexError as e:
            if self.development:
                self.add('encryption_password', 'development_unsecured_password')
                password = 'development_unsecured_password'
            else:
                raise e
        return password

    def init_motor(self):
        raise NotImplemented('No store motor defined.')

    def before_perform_get(self, key):
        if 'decrypted_' in key:
            key = key.replace('decrypted_', '')
        return key

    def after_perform_get(self, key, value):
        if 'decrypted_' in key:
            value = self.decrypt(encrypted_message=value, password=self.get_password())
        return key, value

    def before_perform_set(self, key, value):
        if 'encrypted_' in key:
            key = key.replace('encrypted_', '')
            value = self.encrypt(message=value, password=self.get_password())
        return key, value
