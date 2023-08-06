from abc import abstractmethod, ABCMeta
from typing import Generic, TypeVar, Any, Dict, Callable, NewType, List

from mypy_extensions import NamedArg

from .chain import Entity
# from .2 import Computes, X, ComputeContext, ComputableDict
from .identity import Identity
from .meta import Nature
from .utils import dataclass, Identifier

X = TypeVar('X')
Y = TypeVar('Y')

T = TypeVar('T')

ParameterTypes = Dict[Identifier, Nature]


@dataclass
class SideInfo:
    assumptions: Dict
    depth: int


@dataclass
class ComputationResult(Generic[T]):
    value: T
    side_info: SideInfo


class ComputeContext:
    def resolve_abstract_function(self, abstract_function) -> ComputationResult[Callable]:
        pass

    def with_placeholders(self):
        pass


class Computes(Generic[T], metaclass=ABCMeta):

    @abstractmethod
    def compute(self, context: ComputeContext) -> ComputationResult[T]:
        pass


def dictmap(f, d):
    return {k: f(v) for k, v in d.items()}


def dictval(f, d):
    return [f(v) for v in d.values()]


def side_info_merge(sides: List[SideInfo]) -> SideInfo:
    pass


CD = Dict[Identifier, Any]


@dataclass
class ComputableDict(Computes[CD]):
    data: Dict[Identifier, Computes[Any]]

    def compute(self, context: ComputeContext) -> ComputationResult[CD]:
        res = dictmap(lambda _: _.compute(context), self.data)
        values = dictmap(lambda _: _.value, res)
        side = dictval(lambda _: _.side_info, res)
        return ComputationResult[CD](value=values, side_info=side_info_merge(side))


@dataclass
class FunctionSignature:
    parameters: ParameterTypes
    return_type: Nature
    volatile: bool
    side_effects: bool


@dataclass
class AbstractFunction:
    signature: FunctionSignature
    owner: Identity
    guid: str  # whatever the owner decides it is appropriate


@dataclass
class ComputingAssumptions:
    semantics: str


@dataclass
class EntityStateAssumptions:
    entity_state: Dict[Entity, Any]


@dataclass
class Assumptions:
    entity_state_assumptions: EntityStateAssumptions
    computing_assumptions: ComputingAssumptions


ParametersToUse = NewType('ParametersToUse', Dict[Identifier, Any])


class AbstractFunctionCall(Computes[X]):
    abstract_function: AbstractFunction
    parameters: ComputableDict
    assume: ComputingAssumptions

    def compute(self, context: ComputeContext) -> ComputationResult[X]:
        crf: ComputationResult[Callable[..., X]] = context.resolve_abstract_function(self.abstract_function)
        crp: ComputationResult[CD] = self.parameters.compute(context)
        f = crf.value
        p: Dict[Identifier, Any] = crp.value
        y = f(**p)
        cr = side_info_merge([crf.side_info, crp.side_info])
        return ComputationResult(value=y, side_info=cr)


@dataclass
class FunctionResult:
    fc: AbstractFunctionCall
    data: object
    assume: ComputingAssumptions


from .utils import dataclass, Identifier


@dataclass
class Constant(Computes[T]):
    value: T

    def compute(self, context: ComputeContext) -> ComputationResult[T]:
        side_info = SideInfo({}, 0)
        return ComputationResult(value=self.value, side_info=side_info)


@dataclass
class IfThenElse(Computes[X]):
    """

    Constraints:

        IfThenElse(true, a, b) = a
        IfThenElse(false, a, b) = a

    """
    expr: Computes[bool]
    a: Computes[X]
    b: Computes[X]

    def compute(self, context: ComputeContext) -> ComputationResult[X]:
        eval_expr = self.expr.compute(context=context)
        if eval_expr.value:
            eb = self.a.compute(context=context)
        else:
            eb = self.b.compute(context=context)
        return ComputationResult(eb.value, side_info_merge([eb.side_info, eval_expr.side_info]))


@dataclass
class SelectAttribute(Computes[X], Generic[X, Y]):
    attribute: Identifier
    what: Computes[Y]

    def compute(self, context: ComputeContext) -> ComputationResult[X]:
        cr = self.what.compute(context)
        value = getattr(cr.value, self.attribute)
        return ComputationResult(value, cr.side_info)


@dataclass
class SelectEntry(Computes[X]):
    key: Identifier
    what: Computes[Dict[Identifier, X]]

    def compute(self, context: ComputeContext) -> ComputationResult[X]:
        cr = self.what.compute(context)
        value = cr.value[self.key]
        return ComputationResult(value, cr.side_info)


K = TypeVar('K')
V = TypeVar('V')
W = TypeVar('W')


# f = Callable[[NamedArg(V, name='element')], W]


@dataclass
class DictMap(Computes[Dict[K, W]], Generic[K, V, W]):
    """

    Semantics:

        E{ DictMap(f, x) } = E{ {k: f(v) for k, f in x.items()} }

    For all f, x:

        GetAttribute(att, DictMap(f, x))  = f(GetAttribute(att, x))

    """
    f: Computes[Callable[[V], W]]
    data: Dict[K, Computes[V]]

    def compute(self, context) -> ComputationResult[Dict[K, W]]:
        fres = f.compute(context)

        def apply(v):
            fres

        res = dictmap(lambda _: _.compute(context), self.data)
        values = dictmap(lambda _: _.value, res)
        side = dictval(lambda _: _.side_info, res)
        return ComputationResult[CD](value=values, side_info=side_info_merge(side))

        return {k: self.f(v.compute(context)) for k, v in self.data.items()}


placeholder_guid = NewType('placeholder_guid', str)


@dataclass
class Placeholder(Computes[X]):
    name: Identifier
    guid: placeholder_guid

    def compute(self, context) -> X:
        return context.get_guid(self.guid)


# TemplateParameters = NewType('TemplateParameters', Dict[Identifier, TemplatePlaceholder])


class SpecializeTemplate(Computes[X]):
    """

        # Sub(Template(res, param_spec), parameters)
        # =
        # Template(res / parameters, param_spec - parameters)
        #
        # ## Simplification
        #
        # Template(x, {}) = x

    """
    x: type
    pattern: ComputableDict
    parameters: Dict[Placeholder, Computes[Any]]

    def compute(self, context) -> X:
        context.add(self.parameters)
        atts = self.pattern.compute(context)
        Xi = type(self).__args__[0]
        return Xi(**atts)

#

#
