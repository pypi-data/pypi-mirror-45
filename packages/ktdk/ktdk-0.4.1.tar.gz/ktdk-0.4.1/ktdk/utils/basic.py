"""
Basic object
"""
from json import JSONEncoder

from typing import List


class BasicObject(JSONEncoder):
    """ Base class from which all entities are going to inherit
    """
    BASE_PARAMS = []

    @classmethod
    def base_params(cls) -> List[str]:
        from ktdk import utils
        return utils.bind_class_var(cls, 'BASE_PARAMS')

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return str(self.__class__.__name__) + ": " + str(self.default(o=self))

    def default(self, o):  # pylint: disable=method-hidden
        props = o.__dict__
        if hasattr(o, 'to_dict'):
            props = o.to_dict()
        return props
