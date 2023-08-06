from dataclasses import dataclass

from zuper_schemas.computation import AbstractFunctionCall
from zuper_schemas.monetary import MonetaryValue
from zuper_schemas.timing import TimeInterval
from zuper_schemas.utils import Size


@dataclass
class ExpectType:
    result: object
    typedesc: object  # TypeDescription


@dataclass
class Budget:
    latency: TimeInterval
    storage: Size
    cost: MonetaryValue


@dataclass
class BudgetedFunctionCall:
    actual: AbstractFunctionCall
    function_call: AbstractFunctionCall
