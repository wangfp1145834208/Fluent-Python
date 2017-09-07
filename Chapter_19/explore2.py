from collections import abc
import keyword


class FrozenJSON:
    """使用属性访问法访问JSON数据"""

    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            try:
                attr = self.__data[name]
            except KeyError as exc:
                msg = 'the object has no attribute {!r}'.format(name)
                raise AttributeError(msg) from None
            else:
                return FrozenJSON(attr)

