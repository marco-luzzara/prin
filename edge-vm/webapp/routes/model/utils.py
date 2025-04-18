from typing import Any, TypeVar, Dict, Callable
from dataclasses import fields

T = TypeVar('T') 

def null_if_empty(val: T, transform_fn: Callable[[T], Any] = None):
    if transform_fn is None:
        transform_fn = lambda x: x
    return None if val == '' else transform_fn(val)


def to_float(val: str) -> float:
    val = val.replace(',', '.')
    return float(val)


def from_dict(cls: type[T], obj: Dict[str, Any]) -> T:
    result_dict = {}
    for pr_field in fields(cls):
        dict_key = pr_field.metadata['mapped_to']
        result_dict[pr_field.name] = obj[dict_key]

        if 'transform' in pr_field.metadata:
            result_dict[pr_field.name] = pr_field.metadata['transform'](result_dict[pr_field.name])

    return cls(**result_dict)