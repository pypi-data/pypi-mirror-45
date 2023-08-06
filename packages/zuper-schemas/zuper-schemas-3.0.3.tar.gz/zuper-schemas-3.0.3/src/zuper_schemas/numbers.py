from .utils import dataclass
from typing import NewType, List, ClassVar

DecimalString = NewType('DecimalString', str)


# @dataclass

@dataclass
class Decimal:
    value: DecimalString

    examples: ClassVar[List['Decimal']] = []


Decimal.examples = [
    Decimal(DecimalString('1')),
    Decimal(DecimalString('3.14')),
]
