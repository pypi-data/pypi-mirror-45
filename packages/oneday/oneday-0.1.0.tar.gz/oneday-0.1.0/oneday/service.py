from typing import Type

from oneday import Component
from oneday.exceptions import NotRegisteredError


class Service:
    services = {}

    @classmethod
    def register(cls, original_class: Type):
        annotations: dict = original_class.__init__.__annotations__
        kwargs = {}

        for name, target_type in annotations.items():
            kwargs[name] = Component.get(target_type)

        cls.services[original_class] = original_class(**kwargs)

        return original_class

    @classmethod
    def create(cls, target_class: Type):
        if target_class in cls.services:
            return cls.services[target_class]
        else:
            raise NotRegisteredError(target_class)
