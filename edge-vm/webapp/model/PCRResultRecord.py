from dataclasses import field, fields
from pydantic.dataclasses import dataclass

from typing import Dict, Literal, Any
Self = Any

@dataclass
class PCRResultRecord:
    patient_id: str = field(metadata={'mapped_to': 'Sample Name'})
    target_name: str = field(metadata={'mapped_to': '"Target Name"'})
    mecq: float = field(metadata={'mapped_to': '"Mean Equivalent Cq"'})
    rq: int = field(metadata={'mapped_to': '"Rq"'})
    ddcq: float = field(metadata={'mapped_to': '"DDCq"'})
    