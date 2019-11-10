import pytest
from magic import Miracle, JSON, At

def test_magic_json():
    class MiracleUser(Miracle):
        """ Test User magic class """
        name = At("name")
        age = At("age")


    class MiracleData(Miracle):
        """ Test Data magic class """
        user = At("a", "c", MiracleUser)

    test_input_data = '{"a": {"c": {"name": "Alex", "age": 34}}}'
    user = MiracleData(JSON(test_input_data)).user
    assert user.name == "Alex", "different user names"
    assert user.age == 34, "different user ages"
