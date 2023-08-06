from dataclasses import field
from typing import  *
from .utils import dataclass

PythonPackageName = str


@dataclass
class Version:
    major: str
    minor: str
    patch: str


@dataclass
class Exact:
    exact: Version


@dataclass
class VersionBound:
    minimum_version: Version
    maximum_version: Version


VersionRequirement = Union[Exact, VersionBound]


@dataclass
class PythonRequirement:
    package_name: PythonPackageName
    version_requirement: Optional[VersionRequirement]


@dataclass
class PythonEnvironmentRequirements:
    python_version: VersionRequirement
    package_requirements: List[PythonRequirement] = field(default_factory=[])
