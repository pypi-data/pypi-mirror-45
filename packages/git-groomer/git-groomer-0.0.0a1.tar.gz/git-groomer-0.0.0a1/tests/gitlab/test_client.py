import pytest

from git_groomer.base.exceptions import AuthFailedException, UnknownResponseException


def test_gitlab_client_make_headers_no_apitoken_ko(mock_gitlab_client):
    mock_gitlab_client._api_token = None
    with pytest.raises(AuthFailedException):
        mock_gitlab_client._make_headers()


def test_gitlab_client_make_headers_ok(mock_gitlab_client):
    mock_gitlab_client._api_token = 'test'
    assert mock_gitlab_client._make_headers() == {'PRIVATE-TOKEN': 'test'}


def test_gitlab_client_get_raw_branches_ok(mock_gitlab_client, requests_mock):
    requests_mock.get(f"{mock_gitlab_client.base_url}/repository/branches", json={}, status_code=200)
    result = mock_gitlab_client._get_raw_branches()
    assert result == {}


def test_gitlab_client_get_raw_branches_auth_ko(mock_gitlab_client, requests_mock):
    requests_mock.get(f"{mock_gitlab_client.base_url}/repository/branches", json={}, status_code=401)
    with pytest.raises(AuthFailedException):
        mock_gitlab_client._get_raw_branches()


def test_gitlab_client_get_raw_branches_unknown_response_code_ko(mock_gitlab_client, requests_mock):
    exception_json = {'test': 'test'}
    requests_mock.get(f"{mock_gitlab_client.base_url}/repository/branches", json=exception_json, status_code=100)
    with pytest.raises(UnknownResponseException) as e:
        mock_gitlab_client._get_raw_branches()
        assert e.reponse.json() == exception_json


def test_gitlab_client_delete_branches_ok(mock_gitlab_client, requests_mock):
    branch_name = 'test'
    requests_mock.delete(f"{mock_gitlab_client.base_url}/repository/branches/{branch_name}", text='', status_code=204)
    assert mock_gitlab_client._delete_branch(branch_name) is True


def test_gitlab_client_delete_branches_auth_ko(mock_gitlab_client, requests_mock):
    branch_name = 'test'
    requests_mock.delete(f"{mock_gitlab_client.base_url}/repository/branches/{branch_name}", text='', status_code=401)
    with pytest.raises(AuthFailedException):
        mock_gitlab_client._delete_branch(branch_name)


def test_gitlab_client_delete_branches_unknown_response_code_ko(mock_gitlab_client, requests_mock):
    branch_name = 'test'
    requests_mock.delete(f"{mock_gitlab_client.base_url}/repository/branches/{branch_name}", text='', status_code=100)
    with pytest.raises(UnknownResponseException):
        mock_gitlab_client._delete_branch(branch_name)


def test_gitlab_client_parse_branch_ok(mock_gitlab_client, mock_gitlab_branch):
    branch = mock_gitlab_client._parse_branch(mock_gitlab_branch)
    assert branch.name == mock_gitlab_branch['name']


def test_gitlab_client_parse_branch_commit_ok(mock_gitlab_client, mock_gitlab_branch, mock_gitlab_commit):
    branch = mock_gitlab_client._parse_branch(mock_gitlab_branch)
    commit = branch.last_commit
    assert commit.long_id == mock_gitlab_commit['id']
