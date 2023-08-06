from .utils import dataclass
from typing import NewType, ClassVar, List

from zuper_schemas.numbers import Decimal, DecimalString

UnitString = NewType('UnitString', str)


@dataclass
class Unit:
    name: UnitString

    examples: ClassVar[List['Unit']] = []


Unit.examples = [
    Unit(UnitString('m')),
    Unit(UnitString('m/s'))
]


@dataclass
class UnitQuantity:
    value: Decimal
    units: Unit

    examples: ClassVar[List['UnitQuantity']] = []


UnitQuantity.examples = [
    UnitQuantity(Decimal(DecimalString('12')), Unit(UnitString('m'))),
    UnitQuantity(Decimal(DecimalString('12.1')), Unit(UnitString('m/s')))
]
