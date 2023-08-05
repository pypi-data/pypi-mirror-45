from typing import Type
from oneday.exceptions import NotAddedError


class Component:
    components = {}

    @classmethod
    def get(cls, target_type: Type):
        if target_type in cls.components:
            return cls.components[target_type]
        else:
            raise NotAddedError(target_type)

    @classmethod
    def add(cls, obj, specific_type=None):
        target_type = specific_type or type(obj)
        cls.components[target_type] = obj
