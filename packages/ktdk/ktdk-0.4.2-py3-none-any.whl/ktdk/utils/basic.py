"""
Basic object
"""
from typing import List

from ktdk.utils.serialization import DumpMixin


class BasicObject(DumpMixin):
    """ Base class from which all entities are going to inherit
    """
    BASE_PARAMS = []

    @classmethod
    def base_params(cls) -> List[str]:
        from ktdk import utils
        return utils.bind_class_var(cls, 'BASE_PARAMS')


