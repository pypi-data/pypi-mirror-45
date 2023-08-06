from typing import Dict, List, Optional

from .timing import Date
from .utils import dataclass, Identifier


@dataclass
class GitUser:
    name: str
    email: str  # email


class GitTreeEntry:
    pass


class GitTree(GitTreeEntry):
    entries: Dict[Identifier, GitTreeEntry]


class GitBlob(GitTreeEntry):
    blob: bytes


@dataclass
class GitCommit:
    commit_sha: str
    tree: GitTree
    parents: List['GitCommit']
    commitDate: Date
    authorDate: Date
    comment: str
    author: GitUser
    committer: Optional[GitUser]


#
# TF = Callable[[NamedArg(int, 'b')], int]
#
#
# def f(g: TF) -> int:
#     return g(2.0) + 2
#
#
# f2: TF = f


@dataclass
class GitRepository:
    branches: Dict[Identifier, GitCommit]
    tags: Dict[Identifier, GitCommit]

#
# diff:
#   ~JobPattern:
#     executable: /App/functions/git/diff
#     parameters:
#       current: /Commit/_/tree
#       previous: /Commit/_/parents/0
#

#
# @GitRepository:
#    branches: @dict(@commit)
#    tags: @dict(@commit)
#
# @GitUser:
#    name: @name
#    email: @email
#
# @Commit:
#    commit_sha: @sha
#    tree: @GitTree
#    parents: @list(@Commit)
#    commitDate: @date
#    authorDate: @date
#    comment: @string
#    author: @GitAuthor
#    committer?: @GitAuthor
#
#    diff:
#      ~JobPattern:
#        executable: /App/functions/git/diff
#        parameters:
#          current: /Commit/_/tree
#          previous: /Commit/_/parents/0
#
#
# @GitTreeEntry:
#
#
# @GitTreeEntry/GitTree:
#    entries: @dict(@GitTreeEntry)
#
# @GitTreeEntry/GitBlob:
#    git_blob: @sha
#    blob: @bytes
