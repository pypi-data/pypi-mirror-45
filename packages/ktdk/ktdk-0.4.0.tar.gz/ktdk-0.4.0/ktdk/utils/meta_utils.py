import importlib
import inspect
from typing import List, Type, Dict


def bind_class_var(cls, name: str) -> List[str]:
    cache_name = f'_CACHE_{name}'
    if not hasattr(cls, cache_name):
        parents = [klass for klass in inspect.getmro(cls) if hasattr(klass, name)]
        collection = []
        for klass in parents:
            collection += getattr(klass, name)
        setattr(cls, cache_name, collection)
    return getattr(cls, cache_name)


def subclasses_by_attr(cls: Type, attr: str) -> List:
    subs = cls.__subclasses__()
    result = []
    if hasattr(cls, attr):
        result.append(cls)
    for klass in subs:
        result.extend(subclasses_by_attr(klass, attr))
    return result


def make_subclasses_register(cls: Type, attr: str) -> Dict:
    subs = subclasses_by_attr(cls, attr)
    register = {}
    for klass in subs:
        selector = getattr(klass, attr)
        if selector is None:
            continue
        if not isinstance(selector, List):
            selector = [selector]
        for select in selector:
            register[select] = klass
    return register


def load_class(klass):
    parts = klass.split('.')
    class_name = parts[-1]
    module_path = ".".join(parts[:-1])
    module = importlib.import_module(module_path)
    my_class = getattr(module, class_name)
    return my_class
