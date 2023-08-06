from typing import NewType

from .physical import UnitQuantity
from .utils import dataclass

ISODateString = NewType('ISODateString', str)


@dataclass
class Date:
    iso: ISODateString


@dataclass
class TimeInterval:
    value: UnitQuantity
