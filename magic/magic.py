""" yet another magic library """
import abc
import json
import inspect


class MagicError(Exception):
    """ base magic exception """

    pass


class BaseMagicAction:
    """ Base class for magic actions """

    def __init__(self, *args):
        self.args = args


class MagicActionsAppliedMetaclass(type):
    """ Metaclass for adding magic attributes.

        class User(Magic):
            name = At("name")
            age = At("age")

        user = User(x)
        print(user.name, user.age)
    """

    def __new__(mcs, name, bases, attrs):
        obj = super(MagicActionsAppliedMetaclass, mcs).__new__(
            mcs, name, bases, attrs
        )
        setattr(obj, "_magic", {})
        for attr, action in obj.__dict__.items():
            if isinstance(action, BaseMagicAction):
                getattr(obj, "_magic")[attr] = action
        return obj

    def __call__(cls, target):
        obj = super(MagicActionsAppliedMetaclass, cls).__call__(target)
        for attr, action in getattr(obj, "_magic").items():
            value_after_magic = action.apply_magic(target)
            if isinstance(value_after_magic, Miracle):
                value = value_after_magic
            else:
                value = value_after_magic.unwrapped
            setattr(obj, attr, value)
        return obj


class Miracle(metaclass=MagicActionsAppliedMetaclass):
    """ Base class for magic-based classes """

    def __init__(self, target):
        pass


class MagicDataConverter(abc.ABC):
    """ abstract method for using different data formats with magic """

    def __init__(self, input_data):
        self._data = self._convert_in(input_data)

    @property
    def unwrapped(self):
        """ python data structure behind MagicDataConverter instance """
        return self._data

    def __str__(self):
        return "{}".format(self.unwrapped)

    @abc.abstractmethod
    def _convert_in(self, input_data):
        """ handle input data """
        ...

    @abc.abstractmethod
    def _convert_out(self, output_data):
        """ convert MagicDataConverter to data back """
        ...


class MagicAction(BaseMagicAction):
    """ Base class for classes with apply_magic method """

    magic_method = "magic"

    def apply_magic(self, target):
        """ Action("a", "b", MiracleUser) """
        for field in self.args:
            if isinstance(field, MagicAction):
                target = field.apply_magic(target)
            elif inspect.isclass(field) and issubclass(field, Miracle):
                return field(target)
            else:
                target = getattr(target, self.magic_method)(field)
        return target


class At(MagicAction):
    """ Magic action for getting data internal fields """

    magic_method = "magic_at"


class JSON(MagicDataConverter):
    """ Handle magic for JSON input """

    def _convert_in(self, input_data):
        return json.loads(input_data)

    def _convert_out(self, output_data):
        return json.dumps(output_data)

    def magic_at(self, key):
        """ implement magic action for At() """
        # TODO optimize object creation
        if isinstance(self.unwrapped, list):
            if isinstance(key, int):
                value = self.unwrapped[key]
            else:
                raise MagicError(
                    "JSON method At needs int key for handle lists"
                )
        elif isinstance(self.unwrapped, dict):
            if not isinstance(key, str):
                raise MagicError(
                    "JSON method At needs str key for handle objects"
                )
            if key not in self.unwrapped:
                raise MagicError("{} doesn't have {} key".format(self, key))
            value = self.unwrapped[key]
        else:
            raise MagicError(
                "JSON method At supports only lists and objects handling"
            )

        return self.__class__(self._convert_out(value))
