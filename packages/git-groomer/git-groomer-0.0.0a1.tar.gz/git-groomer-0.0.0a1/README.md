# Git Groomer
[![CircleCI](https://circleci.com/gh/JavierLuna/git-groomer.svg?style=svg)](https://circleci.com/gh/JavierLuna/git-groomer)
[![codecov](https://codecov.io/gh/JavierLuna/git-groomer/branch/master/graph/badge.svg)](https://codecov.io/gh/JavierLuna/git-groomer)
![versions](https://img.shields.io/badge/Python-3.6%2C%203.7-brightgreen.svg)

Maintain your Git repository with ease.

## Description

Git groomer is a tool to help with Git repository maintaining.

Too many open (and often stale) branches?
Do you have 3 weeks old open hotfixes?
Merged branches are still open?

With git groomer, you can easily filter those kind of branches and delete them automatically.


## Installation

Project will be deployed to PyPi soon.

## Example
````python
from git_groomer.gitlab import GitlabRepository

# You have to have the GITLAB_API_TOKEN environmental variable set with your Gitlab API token.
repo = GitlabRepository(repository_name="Generic repo", repository_id=1234)

merged_branches = repo.filter(merged=True, older_than=4) # Get merged branches, older than 4 days

repo.delete_branches(merged_branches) # Delete them

````