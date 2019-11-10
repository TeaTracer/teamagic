""" yet another magic library """
import abc
import json
import csv
import inspect


class MagicError(Exception):
    """ base magic exception """

    pass


class BaseMagicAction:
    """ Base class for magic actions """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.convertion = kwargs.get("convertion")


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
            elif isinstance(value_after_magic, MagicDataConverter):
                value = value_after_magic.unwrapped
            else:
                value = value_after_magic
            if action.convertion:
                value = action.convertion(value)
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

    def __repr__(self):
        return "{}({})".format(self.__class__, self.unwrapped)

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


class At(MagicAction):
    """ Magic action for getting data internal fields """

    magic_method = "magic_at"

    def apply_magic(self, target):
        """ At("a", "b", MiracleUser)
            At(0)
        """
        for field in self.args:
            if isinstance(field, MagicAction):
                target = field.apply_magic(target)
            elif inspect.isclass(field) and issubclass(field, Miracle):
                return field(target)
            else:
                target = getattr(target, self.magic_method)(field)
        return target


class Each(MagicAction):
    """ Magic action for fetching data iterables """

    magic_method = "magic_each"

    def apply_magic(self, target):
        """ Each(MiracleUser)
        """

        def dummy_func(argument):
            """ return itself """
            return argument

        func = dummy_func
        for field in self.args:
            if isinstance(field, MagicAction):

                def magic_func(argument):
                    """ apply some magic """
                    return field.apply_magic(argument)

                func = magic_func
            elif inspect.isclass(field) and issubclass(field, Miracle):

                def miracle_func(argument):
                    """ pass data to miracle class """
                    return field(argument)

                func = miracle_func
            else:
                raise MagicError("Not implemented")
            break

        return getattr(target, self.magic_method)(func)


class Itself(MagicAction):
    """ Magic action for getting data as is"""

    magic_method = "magic_itself"

    @staticmethod
    def apply_magic(target):
        """ Itself() """
        return target


class JSON(MagicDataConverter):
    """ Handle magic for JSON input """

    def _convert_in(self, input_data):
        return json.loads(input_data)

    def _convert_out(self, output_data):
        return json.dumps(output_data)

    def magic_at(self, key):
        """ implement magic action for At() """
        if isinstance(self.unwrapped, list):
            if isinstance(key, int):
                value = self.unwrapped[key]
            else:
                raise MagicError(
                    "JSON method At needs int key for handle lists"
                    ", not {} {}".format(key, self)
                )
        elif isinstance(self.unwrapped, dict):
            if not isinstance(key, str):
                raise MagicError(
                    "JSON method At needs str key for handle objects"
                    ", not {}".format(key)
                )
            if key not in self.unwrapped:
                raise MagicError("{} doesn't have {} key".format(self, key))
            value = self.unwrapped[key]
        else:
            raise MagicError(
                "JSON method At supports only lists and objects handling"
            )

        return self.__class__(self._convert_out(value))

    def magic_each(self, func):
        """ implement magic action for Each() """
        if isinstance(self.unwrapped, list):
            result = []
            for element in self.unwrapped:
                result.append(func(JSON(self._convert_out(element))))
            return result
        else:
            raise MagicError("JSON method Each supports only lists")

    def magic_itself(self):
        """ implement magic action for Itself() """
        return self


class CSV(MagicDataConverter):
    """ Handle magic for CSV input """

    @staticmethod
    def read_file(fileobj):
        """ convert csv file to list """
        return list(csv.reader(fileobj))

    def _convert_in(self, input_data):
        if hasattr(input_data, "read"):
            return self.read_file(input_data)
        elif isinstance(input_data, str):
            return input_data.split(",")
        elif isinstance(input_data, list):
            return input_data
        else:
            raise MagicError("CSV input types should be file, str or list")

    def _convert_out(self, output_data):
        return output_data

    def magic_at(self, key):
        """ implement magic action for At() """
        if isinstance(self.unwrapped, list):
            if isinstance(key, int):
                value = self.unwrapped[key]
            else:
                raise MagicError(
                    "CSV method At needs int key for handle lists"
                    ", not {} {}".format(key, self)
                )
        else:
            raise MagicError(
                "CSV method At supports only lists and objects handling"
            )

        return value

    def magic_each(self, func):
        """ implement magic action for Each() """
        if isinstance(self.unwrapped, list):
            result = []
            for element in self.unwrapped:
                result.append(func(CSV(self._convert_out(element))))
            return result
        else:
            raise MagicError(
                "CSV method Each supports only lists, not {}".format(
                    self.unwrapped
                )
            )

    def magic_itself(self):
        """ implement magic action for Itself() """
        return self
