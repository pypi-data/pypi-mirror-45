from typing import List, Optional, Dict

from .utils import Identifier, dataclass


@dataclass
class Nature:
    extends: Optional[object]
    json_schema: object


@dataclass
class NatureComposite:
    fields: Dict[Identifier, Nature]


@dataclass
class NatureDict:
    keys: Optional[Nature]
    values: Optional[Nature]


class NaturePrimitive(Nature):
    pass


class NatureInt(NaturePrimitive):
    tests: List[str]  # JSON schema tests


class NatureString(NaturePrimitive):
    tests: List[str]  # String
