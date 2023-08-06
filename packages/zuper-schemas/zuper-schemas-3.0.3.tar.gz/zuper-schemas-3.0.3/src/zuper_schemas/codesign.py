from abc import abstractmethod, ABCMeta
from typing import Dict

from .utils import dataclass, Identifier


@dataclass
class Poset:
    pass


RTuple = Dict[Identifier, Poset]
FTuple = Dict[Identifier, Poset]


@dataclass
class CodesignProblemInterface:
    provides: FTuple
    requires: RTuple


@dataclass
class ConcreteCodesignProblemInterface(CodesignProblemInterface):
    implementation: object


@dataclass
class CodesignProblem(metaclass=ABCMeta):
    interface: CodesignProblemInterface

    @abstractmethod
    def feasibility(self, F: FTuple, R: RTuple):
        pass

    @abstractmethod
    def min_resources(self, F: FTuple, R: RTuple):
        pass

    @abstractmethod
    def max_functionality(self, F: FTuple, R: RTuple):
        pass

@dataclass
class UncertainCodesignProblem:
    u: CodesignProblem
    l: CodesignProblem


class ScalableUncertainCodesignProblem(UncertainCodesignProblem):
    @abstractmethod
    def refine(self) -> UncertainCodesignProblem:
        pass

    @abstractmethod
    def coarsen(self) -> UncertainCodesignProblem:
        pass
