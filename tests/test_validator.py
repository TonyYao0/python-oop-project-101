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