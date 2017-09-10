import abc


class AutoStorage:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)
    
    @abc.abstractmethod
    def validate(self, instance, value):
        """return validated value or raise ValueError"""


class Quantity(Validated):

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        else:
            return value


class NonBlank(Validated):

    def validate(self, instance, value):
        value = value.strip()
        if value == '':
            raise ValueError('value cannot be empty or blank')
        return value


class EntityMeta(type):

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        for key, attr in attr_dict.items():
            if isinstance(attr, Validated):
                type_name = attr.__class__.__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)


class Entity(metaclass=EntityMeta):
    pass

