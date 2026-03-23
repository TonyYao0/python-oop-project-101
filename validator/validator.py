class Validator:
    def string(self):
        return StringSchema()


class StringSchema:
    def __init__(self):
        self.rules = {}
        self._required = False


    def required(self):
        self._required = True
        return self


    def min_len(self, length):
        self.rules['min_len'] = lambda x: len(x) >= length
        return self


    def contains(self, sub):
        self.rules['contains'] = lambda x: sub in x
        return self

    def is_valid(self, value):
        if value is None or '':
            return not self._required

        return all(rule(value) for rule in self.rules.values())



