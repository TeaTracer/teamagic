import pytest
from magic import Miracle, JSON, At

def test_magic_at():
    class MiracleUser(Miracle):
        """ Test User magic class """
        name = At("name")
        age = At("age")


    class MiracleData(Miracle):
        """ Test Data magic class """
        user = At("a", "c", MiracleUser)

    test_input_data = '{"a": {"c": {"name": "Alex", "age": 34}}}'
    user = MiracleData(JSON(test_input_data)).user
    assert user.name == "Alex"
    assert user.age == 34

def test_magic_at_multiple_fields():
    class MiracleUser(Miracle):
        """ Test User magic class """
        name = At("name")
        age = At("other", "age")


    class MiracleData(Miracle):
        """ Test Data magic class """
        user = At("c", MiracleUser)

    test_input_data = '{"c": {"name": "Alex", "other": {"age": 34}}}'
    user = MiracleData(JSON(test_input_data)).user
    assert user.name == "Alex"
    assert user.age == 34
