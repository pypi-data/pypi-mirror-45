from typing import Type


class NotAddedError(Exception):
    def __init__(self, target_type: Type):
        self.target_type = target_type

    def __str__(self):
        return f'Component for type  {self.target_type} not added'
