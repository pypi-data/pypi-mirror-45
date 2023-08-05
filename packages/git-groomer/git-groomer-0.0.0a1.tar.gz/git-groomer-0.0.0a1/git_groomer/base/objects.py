import re
from datetime import datetime
from typing import List, Union

import maya


class Commit:
    def __init__(self, long_id: str = None, author: str = None, title: str = None, message: str = None,
                 created_on: datetime = None,
                 parent_ids: List[str] = None):
        self.long_id = long_id
        self.author = author
        self.message = message
        self.created_on = created_on
        self.parent_ids = parent_ids or []
        self.title = title

    @property
    def short_id(self):
        return self.long_id[:7]

    def __str__(self):
        return f"{self.short_id}\t{self.title}\t{self.author}"

    def __repr__(self):
        return f"<Commit {self.short_id}\t{self.title}\t{self.author} >"


class Branch:
    def __init__(self, name: str, merged: bool = None, last_commit: Commit = None):
        self.name = name
        self.merged = merged
        self.last_commit = last_commit

    def __repr__(self):
        return f"<Branch {self.name} >"

    def __str__(self):
        return self.name


class Repository:
    def __init__(self, name: str, git_client):
        self.name = name
        self.git_client = git_client
        self._branches = None

    @staticmethod
    def filter_branches(branches: List[Branch], author: str = None, older_than: int = None, newer_than: int = None,
                        name: str = None, merged: bool = None) -> List[Branch]:
        filters = []

        if author is not None:
            filters.append(lambda b: b.last_commit.author == author)

        if merged is not None:
            filters.append(lambda b: b.merged == merged)

        if older_than is not None:
            date_cutoff = maya.now() - maya.timedelta(days=older_than)
            date_cutoff = date_cutoff.datetime()
            filters.append(lambda b: b.last_commit.created_on <= date_cutoff)

        if newer_than is not None:
            date_cutoff = maya.now() + maya.timedelta(days=newer_than)
            date_cutoff = date_cutoff.datetime()
            filters.append(lambda b: b.last_commit.created_on >= date_cutoff)

        if name is not None:
            regex = re.compile(name)
            filters.append(lambda b: regex.match(b.name))

        return [branch for branch in branches if all(f(branch) for f in filters)] if filters else branches

    def filter(self, author: str = None, older_than: int = None, newer_than: int = None, name: str = None,
               merged: bool = None):
        return self.filter_branches(self.branches, author=author, older_than=older_than, newer_than=newer_than,
                                    name=name, merged=merged)

    @property
    def branches(self):
        if self._branches is None:
            self.update_branches()
        return self._branches

    def update_branches(self):
        self._branches = self.git_client.get_branches()

    def delete_branches(self, branches: List[Union[Branch, str]]) -> List[bool]:
        return self.git_client.delete_branches(branches)
