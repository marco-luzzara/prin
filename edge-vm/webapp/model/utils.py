from typing import Any, TypeVar, Dict
from dataclasses import fields

T = TypeVar('T') 

def from_dict(cls: type[T], dict_to_map: Dict[str, Any]) -> T:
    result_dict = {}
    for pr_field in fields(cls):
        dict_key = pr_field.metadata['mapped_to']
        result_dict[pr_field.name] = dict_to_map[dict_key]

        if 'transform' in pr_field.metadata:
            result_dict[pr_field.name] = pr_field.metadata['transform'](result_dict[pr_field.name])

    return cls(**result_dict)