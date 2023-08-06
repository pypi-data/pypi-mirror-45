# from abc import ABCMeta, abstractmethod
#
# from dataclasses import dataclass
# from typing import *
#
# X = TypeVar('X')
#
#
# def example():
#     @dataclass
#     class User:
#         age: int
#         name: str
#
#     def load(name: str) -> User:
#         pass
#
#     def youngest(u1: User, u2: User):
#         if u1.age < u2.age:
#             return u1
#         else:
#             return u2
#
#     def family_young() -> User:
#         u1 = load('u1')
#         u2 = load('u2')
#         return youngest(u1, u2)
#
#     # Proof[ family_young = X ]:
#     #   Proof[ load('u1') = X ] +
#     #   Proof[ load('u2') = Y | load('u1') = X  ] +
#     #   Proof[ X.age < Y.age | load('u1') = Y AND load('u2') = X  ]
#     # OR
#     #   Proof[ load('u1') = Z ] +
#     #   Proof[ load('u2') = X | load('u1') = Z  ] +
#     #   Proof[ X.age < Z.age | load('u1') = Y AND load('u2') = X  ]
#
#     # Proof[ X.age < Y.age | load('u1') = X | load('u2') = Y ]
#     # OR Proof[ Y.age < A.age | load('u1') = Y | load('u2') = X ]
#
#     # assuming no side effects:
#
#
#     # Proof[ X.age < Y.age | load('u1') = X, load('u2') = Y ]
#     # OR Proof[ Y.age < A.age | load('u1') = Y, load('u2') = X ]
#
#
#
#
#
# def LEQ(a: X, b: X) -> type:
#     """ The proposition a <= b is a Type"""
#
#     @dataclass
#     class Leq:
#         a: ClassVar[X]
#         b: ClassVar[X]
#         proof: Any
#
#     return Leq
#
#
# def get_proof():
#     why = 'My explanation'
#     return LEQ(1, 2)(proof=why)
#
#
# @dataclass
# class NLEQ(Generic[X]):
#     a: X
#     b: X
#
#
# class Impossible:
#     """ Empty set """
#
#     def __init__(self):
#         assert False
#
#
# class PosetStructure(Generic[X], metaclass=ABCMeta):
#     the_set: ClassVar[Type[X]]
#
#     @abstractmethod
#     def leq(self, a: X, b: X) -> Union[LEQ[X], NLEQ[X]]:
#         ...
#
#
# P = TypeVar('P', bound=PosetStructure)
#
#
# class OppositePoset(PosetStructure[X]):
#     P0: PosetStructure[X]
#
#     def leq(self, a: X, b: X) -> Union[LEQ[X], NLEQ[X]]:
#         return self.P0.leq(b, a)
#
#
# strategy: Callable[[], Prop]
#
#
# def leq(a: P, b: Inv[P]) -> LEQ[P]:
#     P = type(a)
#     assert P.leq(a, b)
#     return LEQ(a, b)
#
#
# def leq_proof(hints) -> Certificate[LEQ[P]]:
#     pass
#
#
# class Integers(Poset):
#     pass
#
#
# P = TypeVar('P', bound=Poset)
#
#
# class PosetRelation(Generic[P]):
#     a: P
#     b: P
#
#
# class VerifiedStatement:
#     statement: Statement
#     proof: Proof
#
#
# def test_1():
#     pass
#
#
# @dataclass
# class Placeholder(Generic[X]):
#     guid: str
