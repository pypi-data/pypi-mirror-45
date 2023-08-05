from typing import List, Union, Optional

import requests

from git_groomer.base.objects import Branch


class BaseGitClient:
    __client_name__ = 'BASE'

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_branches(self) -> List[Branch]:
        raw_branches = self._get_raw_branches()
        return self._parse_branches(raw_branches)

    def _get_raw_branches(self) -> List[dict]:
        raise NotImplementedError  # pragma: no cover

    def _make_headers(self) -> dict:
        raise NotImplementedError  # pragma: no cover

    def _get(self, url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> requests.Response:
        params = params or {}
        headers = headers or self._make_headers()
        response = requests.get(self.base_url + url, params=params, headers=headers)
        return response

    def _delete(self, url: str, headers: Optional[dict] = None) -> requests.Response:
        headers = headers or self._make_headers()
        response = requests.delete(self.base_url + url, headers=headers)
        return response

    def _parse_branches(self, raw_branches: List[dict]) -> List[Branch]:
        return [self._parse_branch(raw_branch) for raw_branch in raw_branches]

    def _parse_branch(self, raw_branch: dict) -> Branch:
        raise NotImplementedError  # pragma: no cover

    def delete_branches(self, branches: List[Union[Branch, str]]) -> List[bool]:
        return [self.delete_single_branch(branch) for branch in branches]

    def delete_single_branch(self, branch: Union[Branch, str]) -> bool:
        branch_name = branch.name if isinstance(branch, Branch) else branch
        return self._delete_branch(branch_name)

    def _delete_branch(self, branch_name: str) -> bool:
        raise NotImplementedError  # pragma: no cover
