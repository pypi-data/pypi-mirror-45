import pytest

from git_groomer.base.objects import Branch

TEST_BASE_URL = 'http://testsarecoolok.com'


@pytest.fixture
def base_git_client():
    from git_groomer.base.client import BaseGitClient
    return BaseGitClient(TEST_BASE_URL)


@pytest.fixture
def mock_make_headers(mocker):
    return mocker.patch('git_groomer.base.client.BaseGitClient._make_headers', return_value={})


@pytest.fixture
def mock_delete_branch(mocker):
    return mocker.patch('git_groomer.base.client.BaseGitClient._delete_branch')


def test_get_branches_get_raw_branches_called(mocker, base_git_client):
    mock_get_raw_branches = mocker.patch('git_groomer.base.client.BaseGitClient._get_raw_branches', return_value=[])
    mocker.patch('git_groomer.base.client.BaseGitClient._parse_branches', return_value=[])
    base_git_client.get_branches()
    mock_get_raw_branches.assert_called_once()


def test_get_branches_parse_branches_called(mocker, base_git_client):
    mocker.patch('git_groomer.base.client.BaseGitClient._get_raw_branches', return_value=[])
    mock_parse_branches = mocker.patch('git_groomer.base.client.BaseGitClient._parse_branches', return_value=[])
    base_git_client.get_branches()
    mock_parse_branches.assert_called_once()


def test_get_no_params_no_headers(mock_make_headers, base_git_client, requests_mock):
    text_response = 'test'
    requests_mock.get(TEST_BASE_URL, text=text_response)
    response = base_git_client._get('', params=None, headers=None)
    assert response.text == text_response


def test_get_no_params_no_headers_make_headers_called(mock_make_headers, base_git_client, requests_mock):
    text_response = 'test'
    requests_mock.get(TEST_BASE_URL, text=text_response)
    base_git_client._get('', params=None, headers=None)
    mock_make_headers.assert_called_once()


def test_get_custom_params_ok(mock_make_headers, base_git_client, requests_mock):
    text_response = 'test'
    requests_mock.get(TEST_BASE_URL + '?foo=bar', text=text_response)
    response = base_git_client._get('', params={'foo': 'bar'}, headers=None)
    assert response.text == text_response


def test_get_custom_headers_make_headers_not_called(mock_make_headers, base_git_client, requests_mock):
    text_response = 'test'
    custom_headers = {'test_header': 'test_header'}
    requests_mock.get(TEST_BASE_URL, text=text_response)
    base_git_client._get('', params=None, headers=custom_headers)
    assert not mock_make_headers.called


def test_get_custom_headers_ok(mocker, base_git_client):
    mock_get = mocker.patch('git_groomer.base.client.requests.get')
    custom_headers = {'test_header': 'test_header'}
    base_git_client._get('', params=None, headers=custom_headers)
    assert mock_get.call_args[1]['headers'] == custom_headers


def test_delete_ok(mock_make_headers, base_git_client, requests_mock):
    text_response = 'test'
    requests_mock.delete(TEST_BASE_URL, text=text_response)
    response = base_git_client._delete('', headers=None)
    assert response.text == text_response


def test_delete_no_headers_make_headers_called(mock_make_headers, base_git_client, requests_mock):
    text_response = 'test'
    requests_mock.delete(TEST_BASE_URL, text=text_response)
    base_git_client._delete('', headers=None)
    mock_make_headers.assert_called_once()


def test_delete_custom_headers_make_headers_not_called(mock_make_headers, base_git_client, requests_mock):
    text_response = 'test'
    custom_headers = {'test_header': 'test_header'}
    requests_mock.delete(TEST_BASE_URL, text=text_response)
    base_git_client._delete('', headers=custom_headers)
    assert not mock_make_headers.called


def test_delete_custom_headers_ok(mocker, base_git_client):
    mock_delete = mocker.patch('git_groomer.base.client.requests.delete')
    custom_headers = {'test_header': 'test_header'}
    base_git_client._delete('', headers=custom_headers)
    assert mock_delete.call_args[1]['headers'] == custom_headers


@pytest.mark.parametrize('n_branches', [0, 1, 20])
def test_parse_branches_calls_parse_branch(mocker, base_git_client, n_branches):
    mock_branch_list = [None] * n_branches
    mock_pase_branch = mocker.patch('git_groomer.base.client.BaseGitClient._parse_branch')
    base_git_client._parse_branches(mock_branch_list)
    assert mock_pase_branch.call_count == n_branches


@pytest.mark.parametrize('n_branches', [0, 1, 20])
def test_delete_branches_calls_delete_single_branch(mocker, base_git_client, n_branches):
    mock_branch_list = [None] * n_branches
    mock_delete_single_branch = mocker.patch('git_groomer.base.client.BaseGitClient.delete_single_branch')
    base_git_client.delete_branches(mock_branch_list)
    assert mock_delete_single_branch.call_count == n_branches


def test_delete_single_branch_string_branch_name_ok(base_git_client, mock_delete_branch):
    branch_name = 'test'
    base_git_client.delete_single_branch(branch_name)
    assert mock_delete_branch.call_args[0][0] == branch_name


def test_delete_single_branch_string_branch_name_delete_branch_called(base_git_client, mock_delete_branch):
    branch_name = 'test'
    base_git_client.delete_single_branch(branch_name)
    mock_delete_branch.assert_called_once()


def test_delete_single_branch_branch_ok(base_git_client, mock_delete_branch):
    mock_branch = Branch('test', True, None)
    base_git_client.delete_single_branch(mock_branch)
    assert mock_delete_branch.call_args[0][0] == mock_branch.name


def test_delete_single_branch_branch_delete_branch_called(base_git_client, mock_delete_branch):
    mock_branch = Branch('test', True, None)
    base_git_client.delete_single_branch(mock_branch)
    mock_delete_branch.assert_called_once()
