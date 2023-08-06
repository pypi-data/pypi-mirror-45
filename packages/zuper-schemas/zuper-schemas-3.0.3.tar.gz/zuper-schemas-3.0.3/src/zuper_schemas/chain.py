import typing
from dataclasses import dataclass
from typing import Optional, Any, List, Union

from zuper_json.zeneric2 import resolve_types
from .crypto import PublicKey, Signed
from .utils import Generic


@dataclass
class SecurityModel:
    # guid: Any
    owner: PublicKey
    writer: PublicKey
    arbiter: PublicKey


X = typing.TypeVar('X')

M = typing.TypeVar('M')

N = typing.TypeVar('N')

Y = typing.TypeVar('Y')

W = typing.TypeVar('W')
Z = typing.TypeVar('Z')


@dataclass
class Entity(Generic[X]):
    guid: str

    security_model: SecurityModel

    forked: 'Optional[Entity[X]]' = None

    parent: 'Optional[Entity[Any]]' = None


resolve_types(Entity)


#
# @dataclass
# class User:
#     name: str
#     born: int
#
#
# class Y(Entity[User]):
#     @classmethod
#     def get_examples(cls, seed=None):
#         pks = PublicKey.get_examples(seed=seed)
#
#         while True:
#             _, pk1 = pks.__next__()
#             _, pk2 = pks.__next__()
#
#             security_model = SecurityModel(owner=pk1, arbiter=pk2)
#             guid = "guid" + str(random.randint(100, 1000))
#             data0 = User(name='John', born=1990)
#             e = Y(guid=guid,
#                   data0=data0,
#                   security_model=security_model)
#             yield guid, e


# setattr(X, 'get_examples', get_examples)
# remember_created_class(Y)


@dataclass
class EntityVersion(Generic[M]):
    entity: Entity[M]
    value: M
    previous: 'Optional[EntityVersion[M]]' = None


# resolve_types(EntityVersion, locals())
# contains the chain of operations

@dataclass
class EntityOperationSetKey:
    key: str
    value: Any


EntityOperation = Union[EntityOperationSetKey]


def apply_operation_inplace(value, operation: EntityOperation):
    if isinstance(operation, EntityOperationSetKey):

        setattr(value, operation.key, operation.value)

    else:
        raise NotImplementedError(operation)


def apply_operation(value: Any, operation: EntityOperation) -> Any:
    import copy
    if isinstance(operation, EntityOperationSetKey):
        value2 = copy.deepcopy(value)
        setattr(value2, operation.key, operation.value)
        return value2

    else:
        raise NotImplementedError(operation)


@dataclass
class VersionChain(Generic[N]):
    operations: List[EntityOperation]
    version: EntityVersion[N]
    previous: 'Optional[VersionChain[N]]' = None


@dataclass
class EntityUpdateProposal(Generic[Y]):
    base: EntityVersion[Y]

    operations: List[EntityOperation]
    # consistent: bool
    depends: 'Optional[EntityUpdateProposal[Y]]' = None


@dataclass
class VersionChainWithAuthors(Generic[Z]):
    version: VersionChain[Z]

    signed_proposals: List[Signed[EntityUpdateProposal[Z]]]
    previous: 'Optional[VersionChainWithAuthors[Z]]' = None


@dataclass
class EntityState(Generic[W]):
    data: W
    v: EntityVersion[W]
    vc: VersionChain[W]
    vca: VersionChainWithAuthors[W]

#
# @dataclass
# class Rejection:
#     operation: EntityUpdateProposal
#     conflicts: Optional[EntityUpdateProposal]
#
#
# @dataclass
# class EntityMerge:
#     entity: Entity
#     previous: Optional['EntityMerge']
#     accepted: List[EntityUpdateProposal]
#     rejected: List[Rejection]

#
# @EntityOperation:AddOwner:
#   owner: @PublicKey
#
# @EntityOperation:RemoveOwner:
#   owner: @PublicKey
#
# @EntityOperation:AddArbiter:
#   owner: @PublicKey
#
# @EntityOperation:RemoveArbiter:
#   owner: @PublicKey
#
# @EntityOperation:AddWriter:
#   owner: @PublicKey
#
# @EntityOperation:RemoveWriter:
#   owner: @PublicKey
#
# @EntityOperation:AddReader:
#   owner: @PublicKey
#
# @EntityOperation:RemoveReader:
#   owner: @PublicKey
