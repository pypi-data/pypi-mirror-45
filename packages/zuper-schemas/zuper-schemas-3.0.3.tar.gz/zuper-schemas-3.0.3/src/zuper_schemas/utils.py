# Need to be run before the imports below
def first_import_zuper_json():
    # noinspection PyUnresolvedReferences
    import zuper_json


first_import_zuper_json()

# noinspection PyUnresolvedReferences
from dataclasses import dataclass
# noinspection PyUnresolvedReferences
from typing import NewType, Generic 

Identifier = NewType('Identifier', str)  # must_be_like_this

Size = NewType('Size', int)
