from enum import Enum


class BaseEnum(Enum):
    def __init__(self, *args):
        self.verbose_name, self._value_ = args[:2]
        self._value2member_map_[self._value_] = self

    @classmethod
    def get_choices(cls):
        return tuple((i._value_, i.verbose_name) for i in cls)

    @classmethod
    def get_name(cls, id):
        return cls(id).name

    @classmethod
    def get_id(cls, name):
        for i in cls:
            if i.verbose_name == name:
                return i._value_
        return None

    @classmethod
    def get_internal(cls, name):
        for i in cls.get_choices():
            if i[0] == name:
                return i[1]
