import os
from typing import List, Optional

import maya

from git_groomer.base.client import BaseGitClient
from git_groomer.base.exceptions import AuthFailedException, UnknownResponseException
from git_groomer.base.objects import Commit, Branch


class GitlabClient(BaseGitClient):
    __client_name__ = 'GitLab'

    def __init__(self, project_id: int, api_token: Optional[str] = None):
        super().__init__(base_url=f'https://gitlab.com/api/v4/projects/{project_id}')
        self._api_token = api_token or os.getenv("GITLAB_API_TOKEN")
        self.project_id = project_id

    def _make_headers(self) -> dict:
        if not self._api_token:
            raise AuthFailedException("Gitlab API token was not provided and request could not be made")
        return {'PRIVATE-TOKEN': self._api_token}

    def _get_raw_branches(self) -> List[dict]:
        response = self._get(f'/repository/branches')
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise AuthFailedException("Gitlab authentication error")
        else:
            raise UnknownResponseException("Unknown response from Gitlab", response)

    def _parse_branch(self, raw_branch: dict) -> Branch:
        last_branch_commit = raw_branch['commit']
        last_branch_commit = Commit(long_id=last_branch_commit['id'],
                                    author=last_branch_commit['author_email'],
                                    title=last_branch_commit['title'], message=last_branch_commit['message'],
                                    created_on=maya.parse(last_branch_commit['authored_date']).datetime(),
                                    parent_ids=last_branch_commit['parent_ids'])
        branch = Branch(name=raw_branch['name'], merged=raw_branch['merged'], last_commit=last_branch_commit)
        return branch

    def _delete_branch(self, branch_name: str) -> bool:
        response = self._delete(f'/repository/branches/{branch_name}')
        if response.status_code == 204:
            return True
        elif response.status_code == 401:
            raise AuthFailedException('Gitlab authentication error')
        else:
            raise UnknownResponseException("Unknown response from Gitlab", response)
