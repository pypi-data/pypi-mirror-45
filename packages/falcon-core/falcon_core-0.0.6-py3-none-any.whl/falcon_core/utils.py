import importlib
import hashlib
import inspect

from falcon_core.config import settings


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


"""
Generate dict from instance
"""


def register_iterable(generator, iterable):
    generator.iterables.append(iterable)


def register_rule(generator, name, rule=None):
    if generator.rules is not None:
        if rule:
            generator.rules.register(name, rule)
        else:
            def wraps_rule(rule):
                generator.rules.register(name, rule)
                return rule

            return wraps_rule


def dict_from_obj(obj, data):
    gdi = DictGenerator(obj, data)
    return gdi.generate()


class Rule:
    generator = None

    def __init__(self, obj, value=None):
        self.obj = obj
        self.value = value

    def generate(self):
        raise NotImplementedError


class Rules(dict):
    generator = None

    def __set_name__(self, owner, name):
        self.generator = owner

    def register(self, name, rule):
        rule.generator = self.generator
        self.update(**{name: rule})


class Generator:
    rules = None

    def generate(self):
        raise NotImplementedError


class DictGenerator(Generator):
    iterables = [list, tuple]
    rules = Rules()

    def __init__(self, obj, data):
        self.obj = obj
        self.data = data

    def generate(self):
        if isinstance(self.obj, tuple(self.iterables)):
            return ObjectsRule(self.obj, self.data).generate()
        return ObjectRule(self.obj, self.data).generate()


@register_rule(DictGenerator, 'string')
class StrRule(Rule):
    def generate(self):
        return str(self.obj)


@register_rule(DictGenerator, 'integer')
class IntRule(Rule):
    def generate(self):
        return int(self.obj)


@register_rule(DictGenerator, 'float')
class FloatRule(Rule):
    def generate(self):
        return float(self.obj)


@register_rule(DictGenerator, 'object')
class ObjectRule(Rule):
    def generate(self):
        data = {}
        for field, rule, *v in self.value:
            field, name = field.split(':') if ':' in field else (field, field)
            if v:
                data[name] = self.generator(getattr(self.obj, field), v[0]).generate()
            else:
                data[name] = self.generator.rules[rule](getattr(self.obj, field)).generate()
        return data


@register_rule(DictGenerator, 'objects')
class ObjectsRule(Rule):
    def generate(self):
        return [ObjectRule(obj_item, self.value).generate() for obj_item in self.obj]
