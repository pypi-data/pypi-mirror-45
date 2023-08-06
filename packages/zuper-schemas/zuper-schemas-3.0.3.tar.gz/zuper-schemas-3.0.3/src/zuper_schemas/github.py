from typing import *

from zuper_schemas.git import GitRepository
from zuper_schemas.network import URL
from zuper_schemas.timing import Date
from .utils import dataclass, Identifier


@dataclass
class GithubView:
    organizations: Dict[str, 'GithubOrganization']


@dataclass
class GithubUser:
    id: int
    url: URL
    gravatar_id: Optional[str]

    #
    # organization_self: GithubOrganization
    # organizations: Set[GithubOrganization]


@dataclass
class GithubRepository:
    id: int
    node_id: str
    full_name: str
    private: bool
    # fork: Optional['GithubFork']
    visibility: str
    creator: GithubUser
    created: Date
    updated: Date

    fork_count: int
    watchers_count: int

    git_repository: GitRepository

#
# @dataclass
# class GithubFork:
#     repository: GithubRepository
#     repository_version: Any


@dataclass
class GithubOrganization:
    id: int
    node_id: str
    url: URL
    avatar_url: URL

    repositories: Dict[Identifier, GithubRepository]


@dataclass
class GithubCredentials:
    username: str
    password: str


class UIProxy():
    def ask(self, msg) -> Dict[str, str]:
        pass


def get_user_proxy() -> UIProxy:
    pass


# @sideeffect
def ask_user_credentials():
    msg = 'Please write your username and password'
    uiproxy = get_user_proxy()
    res = uiproxy.ask(msg)
    username = res['username']
    password = res['password']
    return GithubCredentials(username, password)


# def get_github_view() -> GithubView:
#     credentials = ask_user_credentials()
#     authenticate = None
#     view = authenticate(credentials)
#     return view
