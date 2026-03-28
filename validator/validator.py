class Schema():
    def __init__(self, custom_validators=None, data_type=None):
        self.rules = {}
        self._required = False
        self.custom_validators = custom_validators or {}
        self.data_type = data_type

    def test(self, name, arg):
        if name in self.custom_validators:
            fn = self.custom_validators[name]
            self.rules[name] = lambda x: fn(x, arg)
        return self


    def required(self):
        self._required = True
        return self

    def is_valid(self, value):
        if value is None or value == '':
            return not self._required
        if self.data_type and not isinstance(value, self.data_type):
            return False
        return all(rule(value) for rule in self.rules.values())


class StringSchema(Schema):
    def min_len(self, length):
        self.rules['min_len'] = lambda x: len(x) >= length
        return self


    def contains(self, sub):
        self.rules['contains'] = lambda x: sub in x
        return self


class NumberSchema(Schema):
    def positive(self):
        self.rules['positive'] = lambda x: x > 0
        return self


    def range(self, n_min, n_max):
        self.rules['range'] = lambda x: n_min <= x <= n_max
        return self


class ListSchema(Schema):
    def sizeof(self, value):
        self.rules['sizeof'] = lambda x: len(x) == value
        return self


class DictSchema(Schema):
    def __init__(self, custom_validators=None, data_type=None):
        super().__init__(custom_validators, data_type)
        self.rules_map = None


    def shape(self, rules_map):
        self.rules_map = rules_map
        return self

    def is_valid(self, value):
        if not super().is_valid(value):
            return False
        if value is None:
            return True
        if self.rules_map:
            for key, schema in self.rules_map.items():
                if not schema.is_valid(value.get(key)):
                    return False
        return True


class Validator:
    def __init__(self):
        self.registry = {
            'string': {},
            'number': {},
            'list': {},
            'dict': {}
        }

    def add_validator(self, data_type, name, fn):
        self.registry[data_type][name] = fn

    def dict(self):
        return DictSchema(self.registry['dict'], dict)

    def string(self):
        return StringSchema(self.registry['string'], str)

    def number(self):
        return NumberSchema(self.registry['number'], (int, float))

    def list(self):
        return ListSchema(self.registry['list'], list)
