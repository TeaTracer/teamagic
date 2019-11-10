from magic import Miracle, JSON, CSV, At, Each, Itself


def test_magic_at():
    class MiracleUser(Miracle):
        name = At("name")
        age = At("age")

    class MiracleData(Miracle):
        user = At("a", "c", MiracleUser)

    test_input_data = '{"a": {"c": {"name": "Alex", "age": 34}}}'
    user = MiracleData(JSON(test_input_data)).user
    assert user.name == "Alex"
    assert user.age == 34


def test_magic_at_multiple_fields():
    class MiracleUser(Miracle):
        name = At("name")
        age = At("other", "age")

    class MiracleData(Miracle):
        user = At("c", MiracleUser)

    test_input_data = '{"c": {"name": "Alex", "other": {"age": 34}}}'
    user = MiracleData(JSON(test_input_data)).user
    assert user.name == "Alex"
    assert user.age == 34


def test_magic_at_positional():
    class MiracleUser(Miracle):
        name = At(0)
        age = At(1)

    test_input_data = '["Alex", 34]'
    user = MiracleUser(JSON(test_input_data))
    assert user.name == "Alex"
    assert user.age == 34


def test_magic_each():
    class MiracleUser(Miracle):
        name = At("name")

    class MiracleData(Miracle):
        users = Each(MiracleUser)

    test_input_data = '[{"name": "Alex"}, {"name": "Den"}]'
    users = MiracleData(JSON(test_input_data)).users
    assert users[0].name == "Alex"
    assert users[1].name == "Den"


def test_itself():
    class MiracleUser(Miracle):
        name = Itself()

    test_input_data = '"Alex"'
    user = MiracleUser(JSON(test_input_data))
    assert user.name == "Alex"


def test_itself_double():
    class MiracleUser(Miracle):
        name = Itself()
        name_bkp = Itself()

    test_input_data = '"Alex"'
    user = MiracleUser(JSON(test_input_data))
    assert user.name == "Alex"
    assert user.name_bkp == "Alex"


def test_magic_each_positional():
    class MiracleUser(Miracle):
        name = Itself()

    class MiracleData(Miracle):
        users = Each(MiracleUser)

    test_input_data = '["Alex", "Den"]'
    users = MiracleData(JSON(test_input_data)).users
    assert users[0].name == "Alex"
    assert users[1].name == "Den"


def test_magic_each_each():
    class MiracleUser(Miracle):
        name = At("name")

    class MiracleUsers(Miracle):
        users = Each(MiracleUser)

    class MiracleData(Miracle):
        users = Each(MiracleUsers)

    test_input_data = (
        '[[{"name": "Alex"}, {"name": "Den"}], [{"name": "Brad"}]]'
    )
    users = MiracleData(JSON(test_input_data)).users
    assert users[0].users[0].name == "Alex"
    assert users[0].users[1].name == "Den"
    assert users[1].users[0].name == "Brad"


def test_magic_at_csv():
    class MiracleUser(Miracle):
        name = At(0)
        age = At(1, convertion=int)

    class MiracleData(Miracle):
        users = Each(MiracleUser)

    with open("tests/csv_test.csv") as csv_file:
        users = MiracleData(CSV(csv_file)).users
    assert users[0].name == "Alex"
    assert users[0].age == 34
    assert users[1].name == "Den"
    assert users[1].age == 22
