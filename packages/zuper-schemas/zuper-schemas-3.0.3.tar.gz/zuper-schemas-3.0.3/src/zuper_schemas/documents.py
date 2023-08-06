from typing import *

from zuper_schemas.timing import Date
from .utils import dataclass


@dataclass
class TypedData:
    mime: str
    size: int
    content: bytes


@dataclass
class LanguageSpec:
    code: str


@dataclass
class Translated:
    language: LanguageSpec
    value: str
    translated_from: Optional[Any]


@dataclass
class LocalizableString:
    entries: List[Translated]


@dataclass
class Header:
    long: LocalizableString
    short: Optional[LocalizableString]


@dataclass
class IndexInfo:
    number: bool
    appear_in_toc: bool


@dataclass
class BlockElement:
    pass


@dataclass
class Section:
    index_info: IndexInfo
    title: Optional[Header]
    before: Optional[List[BlockElement]]
    sections: List['Section']  # XXX
    after: Optional[List[BlockElement]]


@dataclass
class AuthorCredit:
    name: str
    affiliation: Optional[str]


@dataclass
class Document:
    title: Optional[Header]
    subtitle: Optional[LocalizableString]
    authors: Optional[List[AuthorCredit]]
    date: Optional[Date]
    sections: List[LocalizableString]


@dataclass
class ParagraphElement:
    pass


@dataclass
class Paragraph(BlockElement):
    translations: Dict[str, 'Paragraph']
    elements: List[ParagraphElement]


@dataclass
class TextFragment(ParagraphElement):
    words: List[str]


@dataclass
class Figure(BlockElement):
    index_info: IndexInfo
    caption: Optional[Paragraph]
    contents: List[ParagraphElement]


@dataclass
class RasterImage:
    width: int
    height: int
    image_data: TypedData


@dataclass
class PlaceImage(BlockElement):
    image: RasterImage
