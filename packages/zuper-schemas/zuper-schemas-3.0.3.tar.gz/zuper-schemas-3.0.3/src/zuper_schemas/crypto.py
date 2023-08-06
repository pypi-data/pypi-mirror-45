# import zuper_json
from datetime import datetime
from typing import *

from zuper_json.zeneric2 import resolve_types
from .utils import dataclass, Generic

if TYPE_CHECKING:
    from dataclasses import dataclass

X = TypeVar('X')


@dataclass
class PublicKey:
    ID: str  # Qm....
    pem: str

    # recovery: 'Optional[EncryptedClearType[Any]]' = None


@dataclass
class EncryptedClearType(Generic[X]):
    pub: PublicKey
    encrypted_session_key: bytes
    ciphertext: bytes
    tag: bytes
    nonce: bytes


@dataclass
class PrivateKey:
    ID: str # hash of public key
    pem: str


refs = (PublicKey, PrivateKey, EncryptedClearType)
resolve_types(EncryptedClearType, refs=refs)
resolve_types(PublicKey, refs=refs)
# print('OK here')


@dataclass
class Signed(Generic[X]):
    pub: PublicKey
    sig: bytes
    data: X
    time: datetime


@dataclass
class Pin(Generic[X]):
    data: X
    valid_from: datetime
    valid_to: datetime

#
# @dataclass
# class SymmetricKey:
#     key: bytes
#
#
# @dataclass
# class SymmetricallyEncrypted(Generic[X]):
#     key_hash: Multihash
#     encoded: bytes
