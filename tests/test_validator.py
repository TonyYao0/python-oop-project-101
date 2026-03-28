from validator import Validator


def test_string_validator():
    v = Validator()
    schema = v.string()


    assert schema.is_valid('') is True
    assert schema.is_valid(None) is True
    assert schema.is_valid('string') is True


    schema.required()
    assert schema.is_valid('') is False
    assert schema.is_valid('') is False
    assert schema.is_valid('string') is True

    assert schema.contains('s').is_valid('string') is True
    assert schema.contains('x').is_valid('string') is False

    schema2 = v.string().min_len(10).min_len(4)
    assert schema2.is_valid('string') is True

    schema3 = v.string().min_len(4).min_len(10)
    assert schema3.is_valid('string') is False


def test_number_validator():
    v = Validator()
    schema = v.number()
    assert schema.is_valid(None) is True

    schema.required()
    assert schema.is_valid(None) is False
    assert schema.is_valid(0) is True

    assert schema.is_valid(7) is True

    assert schema.positive().is_valid(7) is True
    assert schema.positive().is_valid(-7) is False

    schema.range(-5, 5)
    assert schema.is_valid(-5) is False
    assert schema.is_valid(5) is True

    schema2 = v.number().positive().range(10, 20).range(5, 15)
    assert schema2.is_valid(7) is True 
    assert schema2.is_valid(17) is False


def test_list_validator():
    v = Validator()
    schema = v.list()
    assert schema.is_valid(None) is True

    schema = schema.required()
    assert schema.is_valid(None) is False
    assert schema.is_valid([]) is True
    assert schema.is_valid(['hexlet']) is True

    assert schema.sizeof(2).is_valid(['hexlet']) is False
    assert schema.sizeof(2).is_valid(['hexlet', 'code-basics']) is True

def test_dict_validator():
    v = Validator()
    schema = v.dict()
    schema.shape({
        'name': v.string().required(),
        'age': v.number().positive(),
    })

    assert schema.is_valid({'name': 'kolya', 'age': 100})  is True
    assert schema.is_valid({'name': 'maya', 'age': None})  is True
    assert schema.is_valid({'name': '', 'age': None})  is False
    assert schema.is_valid({'name': 'ada', 'age': -5})  is False

def test_add_validator():
    v = Validator()
    fn = lambda value, start: value.startswith(start)
    v.add_validator('string', 'startWith', fn)

    schema = v.string().test('startWith', 'H')
    assert schema.is_valid('exlet') is False
    assert schema.is_valid('Hexlet') is True

    fn = lambda value, min: value >= min
    v.add_validator('number', 'min', fn)

    schema = v.number().test('min', 5)
    assert schema.is_valid(4) is False
    assert schema.is_valid(6) is True