from git_groomer.gitlab.objects import GitlabRepository


def test_gitlab_repository_name_ok():
    # This object is more of a sugar thing than functionality but ok
    repository_name = 'Test repo'
    repository_id = 1234
    gitlab_repo = GitlabRepository(repository_name, repository_id=repository_id)
    assert gitlab_repo.name == repository_name


def test_gitlab_repository_id_ok():
    # This object is more of a sugar thing than functionality but ok
    repository_name = 'Test repo'
    repository_id = 1234
    gitlab_repo = GitlabRepository(repository_name, repository_id=repository_id)
    assert gitlab_repo.git_client.project_id == repository_id
