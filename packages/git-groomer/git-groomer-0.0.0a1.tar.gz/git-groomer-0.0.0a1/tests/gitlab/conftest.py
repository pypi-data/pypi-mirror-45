import pytest

from git_groomer.gitlab.client import GitlabClient


@pytest.fixture
def mock_gitlab_client():
    return GitlabClient(1, api_token='test')


@pytest.fixture
def mock_gitlab_commit():
    return {
        "author_email": "john@example.com",
        "author_name": "John Smith",
        "authored_date": "2012-06-27T05:51:39-07:00",
        "committed_date": "2012-06-28T03:44:20-07:00",
        "committer_email": "john@example.com",
        "committer_name": "John Smith",
        "id": "7b5c3cc8be40ee161ae89a06bba6229da1032a0c",
        "short_id": "7b5c3cc",
        "title": "add projects API",
        "message": "add projects API",
        "parent_ids": [
            "4ad91d3c1144c406e50c7b33bae684bd6837faf8"
        ]
    }


@pytest.fixture
def mock_gitlab_branch(mock_gitlab_commit):
    return {
        "name": "master",
        "merged": False,
        "protected": True,
        "default": True,
        "developers_can_push": False,
        "developers_can_merge": False,
        "can_push": True,
        "commit": mock_gitlab_commit
    }
