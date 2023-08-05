import importlib
import hashlib
import inspect

from falcon_core.config import settings
from falcon_core.rules import Rules


def import_object(m):
    m = m.split('.')
    return getattr(importlib.import_module('.'.join(m[:-1])), m[-1], None)


def load_middleware(m):
    m = import_object(m)
    if inspect.isclass(m):
        return m()
    return m


def flatten(l):
    f = []
    for i in l:
        if isinstance(i, (list, tuple)):
            f.extend(flatten(i))
        else:
            f.append(i)
    return f


def encrypt_sha1(text):
    return hashlib.sha1(str(text).encode()).hexdigest()


def encrypt_sha256(text):
    return hashlib.sha256(str(text).encode()).hexdigest()


def encrypt_sha1_with_secret_key(text):
    return encrypt_sha1(text + settings.SECRET_KEY)


def encrypt_sha256_with_secret_key(text):
    return encrypt_sha256(text + settings.SECRET_KEY)


def dict_from_obj(obj, extras, iterable=False):
    rule = ('object', 'objects')[int(iterable)]
    return Rules.execute(obj, rule, extras)
