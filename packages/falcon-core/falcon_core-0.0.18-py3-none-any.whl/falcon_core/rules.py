class Rule:
    def __init__(self, obj, extras=None):
        self.obj = obj
        self.extras = extras

    def get(self, name):
        name, *extras = name.split('.')
        attr = getattr(self.obj, name)
        for extra in extras:
            attr = getattr(attr, extra)
        return attr

    @classmethod
    def setup(cls, obj, extras=None):
        return cls(obj, extras)

    def execute(self):
        raise NotImplementedError


class Rules:
    _rules = {}

    @classmethod
    def all(cls):
        return cls._rules

    @classmethod
    def get(cls, name, default=None):
        return cls.all().get(name, default)

    @classmethod
    def register(cls, name, rule=None):
        if rule:
            cls._rules.update(**{name: rule})
        else:
            def wraps_rule(rule):
                cls._rules.update(**{name: rule})
                return rule

            return wraps_rule

    @classmethod
    def execute(cls, obj, rule, extras=None):
        rule = cls.get(rule)
        if rule:
            return rule.setup(obj, extras).execute()
        raise KeyError


@Rules.register('original')
class OriginalRule(Rule):
    def execute(self):
        return self.obj


@Rules.register('string')
class StrRule(Rule):
    def execute(self):
        if self.obj is not None:
            return str(self.obj)
        return None


@Rules.register('integer')
class IntRule(Rule):
    def execute(self):
        if self.obj is not None:
            return int(self.obj)
        return None


@Rules.register('float')
class FloatRule(Rule):
    def execute(self):
        if self.obj is not None:
            return float(self.obj)
        return None


@Rules.register('boolean')
class BoolRule(Rule):
    def execute(self):
        if self.obj is not None:
            return bool(self.obj)
        return None


@Rules.register('list')
class ListRule(Rule):
    def execute(self):
        if self.obj is not None:
            return list(self.obj)
        return None


@Rules.register('dict')
class DictRule(Rule):
    def execute(self):
        if self.obj is not None:
            return dict(self.obj)
        return None


@Rules.register('object')
class ObjectRule(Rule):
    def execute(self):
        if self.obj:
            data = {}
            for attr, rule, *extras in self.extras:
                attr, name = attr.split(':') if ':' in attr else (attr, attr)
                data[name] = Rules.execute(self.get(attr), rule, *extras)
            return data
        return None


@Rules.register('objects')
class ObjectsRule(Rule):
    def execute(self):
        return [Rules.execute(obj, 'object', self.extras) for obj in self.obj]


@Rules.register('c_object')
class CreateObjectRule(Rule):
    def execute(self):
        cls, self.extras = self.extras
        if self.extras:
            instance = cls()
            for name, rule, *extras in self.extras:
                name, require = name.split(':') if ':' in name else (name, False)
                if hasattr(instance, name):
                    if require and name not in self.obj:
                        return None
                    if name in self.obj:
                        setattr(instance, name, Rules.execute(self.obj.get(name), rule, *extras))
            return instance
        return None


@Rules.register('c_objects')
class CreateObjectRule(Rule):
    def execute(self):
        if self.obj:
            return [Rules.execute(obj, 'c_object', self.extras) for obj in self.obj]
        return None
