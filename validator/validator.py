class Schema():
    def __init__(self):
        self.rules = {}
        self._required = False


    def required(self):
        self._required = True
        return self


class StringSchema(Schema):
    def min_len(self, length):
        self.rules['min_len'] = lambda x: len(x) >= length
        return self


    def contains(self, sub):
        self.rules['contains'] = lambda x: sub in x
        return self

    def is_valid(self, value):
        if value is None or value == '':
            return not self._required
        return all(rule(value) for rule in self.rules.values())


class NumberSchema(Schema):
    def positive(self):
        self.rules['positive'] = lambda x: x > 0
        return self


    def range(self, n_min, n_max):
        self.rules['range'] = lambda x: n_min <= x <= n_max
        return self
    
    def is_valid(self, value):
        if value is None:
            return not self._required
        return all(rule(value) for rule in self.rules.values())


class ListSchema(Schema):
    def sizeof(self, value):
        self.rules['sizeof'] = lambda x: len(x) == value
        return self

    def is_valid(self, value):
        if value is None:
            return not self._required
        if not isinstance(value, list):
            return False
        return all(rule(value) for rule in self.rules.values())

class DickSchema(Schema):
    def shape(self, rules_map):
        self.rules['shape'] = rules_map
        return self

    def is_valid(self, value):
        if value is None:
            return not self._required
        if not isinstance(value, dict):
            return False
        if 'shape' not in self.rules:
            return True
        shape_rules = self.rules['shape']
        for key, schema  in shape_rules.items():
            if not schema.is_valid(value.get(key)):
                return False
        return True


class Validator:
    def dict(self):
        return DickSchema()


    def string(self):
        return StringSchema()

    def number(self):
        return NumberSchema()

    def list(self):
        return ListSchema()
