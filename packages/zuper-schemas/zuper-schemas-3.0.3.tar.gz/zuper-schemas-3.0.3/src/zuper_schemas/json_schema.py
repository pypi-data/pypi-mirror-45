from typing import ClassVar, Optional, Any, List, Dict, Union

from .utils import dataclass


@dataclass
class JSONSchema:
    _dollar_schema: ClassVar[str] = "http://json-schema.org/schema#"
    title: Optional[str]
    description: Optional[str]
    default: Optional[Any]
    examples: List[Any]

    enum: Optional[List]
    const: Optional[Any]

    definitions: Optional[Dict[str, 'JSONSchema']]


@dataclass
class JSONSchemaInt(JSONSchema):
    _type: ClassVar[str] = "int"
    multipleOf: int


@dataclass
class JSONSchemaBool(JSONSchema):
    _type: ClassVar[str] = "boolean"


@dataclass
class JSONSchemaNull(JSONSchema):
    _type: ClassVar[str] = "null"


@dataclass
class JSONSchemaNumber(JSONSchema):
    _type: ClassVar[str] = "number"
    multipleOf: float
    minimum: Optional[float]
    maximum: Optional[float]
    exclusiveMinimum: Optional[bool]
    exclusiveMaximum: Optional[bool]


pattern = str


@dataclass
class JSONSchemaArray(JSONSchema):
    _type: ClassVar[str] = "array"
    items: Optional[Union[JSONSchema, List[JSONSchema]]]
    contains: Optional[JSONSchema]
    additionalItems: Optional[bool]
    minItems: Optional[int]
    maxItems: Optional[int]
    uniqueItems: Optional[bool]


@dataclass
class JSONSchemaString(JSONSchema):
    _type: ClassVar[str] = "string"
    pattern: Optional[pattern]
    maxLength: Optional[int]
    minLength: Optional[int]
    format: Optional[str]


@dataclass
class JSONSchemaObject(JSONSchema):
    _type: ClassVar[str] = "object"
    required: List[str]
    properties: Dict[str, JSONSchema]
    propertyNames: Optional[JSONSchemaString]
    additionalProperties: Optional[Union[bool, JSONSchema]]  # XXX
    minProperties: Optional[int]
    maxProperties: Optional[int]
    dependencies: Optional[Dict[str, List[str]]]
    patternProperties: Optional[Dict[pattern, JSONSchema]]


@dataclass
class JSONSchemaAnyOf(JSONSchema):
    anyOf: List[JSONSchema]


@dataclass
class JSONSchemaAllOf(JSONSchema):
    allOf: List[JSONSchema]


@dataclass
class JSONSchemaOneOf(JSONSchema):
    oneOf: List[JSONSchema]


@dataclass
class JSONSchemaNot(JSONSchema):
    _not: List[JSONSchema]


@dataclass
class JSONSchemaRef(JSONSchema):
    _dollar_ref: str
