class Validator:
    def string(self):
        return StringSchema()

    def number(self):
        return NumberSchema()


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
