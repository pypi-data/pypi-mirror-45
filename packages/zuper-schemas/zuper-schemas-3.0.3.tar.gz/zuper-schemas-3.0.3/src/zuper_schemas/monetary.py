from zuper_schemas.physical import UnitQuantity, UnitString, Unit
from .utils import dataclass


@dataclass
class MonetaryValue:
    value: UnitQuantity


unit_USD = UnitString('USD')
unit_BTC = UnitString('BTC')

import decimal


def value_USD(x):
    return UnitQuantity(decimal.Decimal(x), Unit(unit_USD))


def value_BTC(x):
    return UnitQuantity(decimal.Decimal(x), Unit(unit_BTC))


def BTC_from_USD(usd: UnitQuantity) -> UnitQuantity:
    pass
