from dataclasses import field
from typing import *

from zuper_json.zeneric2 import resolve_types

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from .utils import dataclass

Filename = NewType('Filename', str)
Filepath = NewType('Filepath', str)


#
# @dataclass
# class DirectoryEntry:
#     ...
#
#
# aº = 0
# a⃖ = 0
# a⃗b = 0
# aᐩ= 0


@dataclass
class File:
    """
        A single file.
    """
    data: bytes = field(repr=False)
    owner: Optional[str] = None
    permissions: Optional[str] = None


@dataclass
class Directory:
    """
        A directory holds other directories and files.
    """
    entries: 'Dict[str, Union[File, Directory]]'
    owner: Optional[str] = None
    permissions: Optional[str] = None

    __depends__ = (File, )


#
#  compiled: Directory
#
#  compiled/entries/created/image

# def directory_view(dirname) -> Directory:
#     node = ...
#     return node.read_directory(dirname)
#
#
# def compile_file(data: bytes) -> bytes:
#     pass
#
#
# def compile(input: Directory) -> Directory:
#     entries = {
#         'out1': File(data=compile_file(input.entries['in1'].data)),
#         'out2': File(data=compile_file(input.entries['in2'].data)),
#         'out3': File(data=compile_file(input.entries['in3'].data)),
#     }
#     return Directory(entries)
#
#
# def get_one_file(dirname: str):
#     input_dir: Directory = directory_view(dirname)
#     outdir: Directory = compile(input_dir)
#
#     return outdir.entries['file3']
