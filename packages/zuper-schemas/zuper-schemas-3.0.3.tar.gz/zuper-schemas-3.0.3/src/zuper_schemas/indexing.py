# language=markdown
"""

# An indexing service


An indexing service function is defined by:

1) A type

2) A query string


For example, suppose that we wanted somebody to keep track of
cached functions.

We have FunctionCalls:

    FC(f, params)

A FunctionResult (FR) is of the type:

    FR(fc, data, assumptions)

For example:

    FR -- fc --> FC
       -- data --> D
       -- assume --> Assumptions

So signed by a computer C we have:

    SFR -fr--> FR --fc--> FC
     |         |---> D
     v         `---> A
     C
"""
from collections import defaultdict
from typing import Callable, TypeVar, Set, Dict, Any
from .utils import Generic, dataclass
# from zuper_schemas.computation import AbstractFunctionCall
from .computation import AbstractFunctionCall, FunctionResult
# from zuper_schemas.core import FunctionResult
from .crypto import Signed, PublicKey

from mypy_extensions import NamedArg

"""
If we want to cache this by result FC we would have

    CachingService:
        thing_nature: @SFR
        key: {fr: fc}

"""

T = TypeVar('T')
K = TypeVar('K')

# accept_interface = Callable[[NamedArg(T, 'candidate')], bool]
# index_interface = Callable[[NamedArg(T, 'candidate')], K]

accept_interface = Any
index_interface = Any

@dataclass
class CachingCriteria(Generic[T, K]):
    accept: accept_interface
    indexby: index_interface


# store_interface = Callable[[NamedArg(T, 'candidate')], bool]
# query_interface = Callable[[NamedArg(K, 'key')], Set[T]]
store_interface =  query_interface = Any

@dataclass
class CachingService(Generic[T, K]):
    criteria: CachingCriteria[T, K]
    # how we are going to get it?
    owner: PublicKey
    store: store_interface
    query: query_interface


def accept_all_SFR(*, candidate: Signed[FunctionResult]) -> bool:
    return True


def index_by_function_call(*, candidate: Signed[FunctionResult]) -> AbstractFunctionCall:
    return candidate.data.fc


fc_caching_criteria = CachingCriteria[Signed[FunctionResult], AbstractFunctionCall](
        accept=accept_all_SFR,
        indexby=index_by_function_call)


class ConcreteCachingService(Generic[T, K]):

    def __init__(self, criteria: CachingCriteria):
        self.values: Dict[K, Set[T]] = defaultdict(set)
        self.owner = None
        self.criteria = criteria

    def store(self, *, candidate: T):
        if self.criteria.accept(candidate=candidate):
            k = self.criteria.indexby(candidate=candidate)
            self.values[k].add(candidate)

    def query(self, *, key: K):
        return self.values[key]

    @classmethod
    def examples(cls, self):
        fc_concrete_service = ConcreteCachingService[Signed[FunctionResult], AbstractFunctionCall](fc_caching_criteria)

"""
    I provide function caching service for command results for $1 / query.

    ~CodesignProblem:
        requires:
            ~RTuple:
                transfer:
                    ~TransferTo:
                        value: 1 USD
                        dest: 
                            $identity
        provides:
            ~FTuple:
                service: 
                    ~FunctionCachingService:
                        caching_service:
                            accumulation_channel:
                            query_channel:
                            ~CachingService:
                                thing_nature: @FunctionCall
                                key: 
                                 ~KeyMultiple:
                                    identifier: fr
                                    child: 
                                        ~KeySingle:
                                            fc

"""

"""

    A cache of CachingServices
    

"""
