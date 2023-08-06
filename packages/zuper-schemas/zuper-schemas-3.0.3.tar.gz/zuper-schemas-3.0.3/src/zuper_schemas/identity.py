from .crypto import PublicKey
from .utils import dataclass


@dataclass
class Identity:
    name: str # any short name
    key: PublicKey

