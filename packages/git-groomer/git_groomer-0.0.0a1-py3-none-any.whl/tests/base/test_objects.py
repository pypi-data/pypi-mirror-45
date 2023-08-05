def test_commit_short_id(mock_commit):
    assert mock_commit.long_id.startswith(mock_commit.short_id)


def test_commit_short_id_in_str(mock_commit):
    assert mock_commit.short_id in str(mock_commit)


def test_commit_title_in_str(mock_commit):
    assert mock_commit.title in str(mock_commit)


def test_commit_author_in_str(mock_commit):
    assert mock_commit.author in str(mock_commit)


def test_commit_short_id_in_repr(mock_commit):
    assert mock_commit.short_id in repr(mock_commit)


def test_commit_title_in_repr(mock_commit):
    assert mock_commit.title in repr(mock_commit)


def test_commit_author_in_repr(mock_commit):
    assert mock_commit.author in repr(mock_commit)


def test_branch_name_is_str(mock_branch):
    assert mock_branch.name == str(mock_branch)


def test_branch_name_in_repr(mock_branch):
    assert mock_branch.name in repr(mock_branch)


def test_repository_branches_lazy_none_on_init(mock_repository):
    assert mock_repository._branches is None


def test_repository_branches_lazy_get_branches_called(mock_repository):
    mock_repository.branches
    assert mock_repository.git_client.get_branches.called


def test_repository_branches_lazy_get_branches_loaded(mock_repository):
    assert mock_repository.branches == []


def test_repository_branches_lazy_get_branches_only_once(mock_repository):
    mock_repository.branches
    mock_repository.branches
    assert mock_repository.git_client.get_branches.call_count == 1


def test_repository_update_branches_ok(mock_repository):
    mock_repository.update_branches()
    assert mock_repository.git_client.get_branches.called


def test_repository_delete_branches_ok(mock_repository):
    mock_repository.delete_branches(["a", "b"])
    assert mock_repository.git_client.delete_branches.called


def test_repository_filter_uses_own_branches(mocker, mock_repository):
    mock_branches = 'test'
    mock_repository._branches = mock_branches
    mock_filter_branches = mocker.patch('git_groomer.base.objects.Repository.filter_branches')
    mock_repository.filter()
    assert mock_filter_branches.call_args[0][0] == mock_branches


def test_repository_filter_branches_empty(mock_repository, mock_branch_pool):
    all_branches = set(mock_branch_pool.values())
    result = mock_repository.filter_branches(all_branches)
    assert result == all_branches


def test_repository_filter_branches_by_author(mock_repository, mock_branch_pool):
    all_branches = set(mock_branch_pool.values())
    result = mock_repository.filter_branches(all_branches, author=mock_branch_pool['author'].last_commit.author)
    assert result == [mock_branch_pool['author']]


def test_repository_filter_branches_by_older_than(mock_repository, mock_branch_pool):
    all_branches = set(mock_branch_pool.values())
    result = mock_repository.filter_branches(all_branches, older_than=1)
    assert result == [mock_branch_pool['older_than']]


def test_repository_filter_branches_by_newer_than(mock_repository, mock_branch_pool):
    all_branches = set(mock_branch_pool.values())
    result = mock_repository.filter_branches(all_branches, newer_than=1)
    assert result == [mock_branch_pool['newer_than']]


def test_repository_filter_branches_by_merged(mock_repository, mock_branch_pool):
    all_branches = set(mock_branch_pool.values())
    result = mock_repository.filter_branches(all_branches, merged=True)
    assert result == [mock_branch_pool['merged']]


def test_repository_filter_branches_by_name_literal_string_regex(mock_repository, mock_branch_pool):
    all_branches = set(mock_branch_pool.values())
    result = mock_repository.filter_branches(all_branches, name='test')
    assert result == [mock_branch_pool['name_string']]


def test_repository_filter_branches_by_name_literal_num_regex(mock_repository, mock_branch_pool):
    all_branches = set(mock_branch_pool.values())
    result = mock_repository.filter_branches(all_branches, name=r'\d')
    assert result == [mock_branch_pool['name_num']]
