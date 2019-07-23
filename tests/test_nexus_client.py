# -*- coding: utf-8 -*-
import pytest

import nexuscli
from nexuscli import exception
from nexuscli.nexus_client import NexusClient


def test_repositories(mocker):
    """
    Ensure that the class fetches repositories on instantiation
    """
    mocker.patch('nexuscli.nexus_client.RepositoryCollection')

    client = NexusClient()

    nexuscli.nexus_client.RepositoryCollection.assert_called()
    client.repositories.refresh.assert_called_once()


@pytest.mark.parametrize(
    'component_path, x_repo, x_dir, x_file', [
        ('some/path/', 'some', 'path', None),
        ('some/other/path/', 'some', 'other/path', None),
        ('some/path/file', 'some', 'path', 'file'),
        ('some/other/path/file', 'some', 'other/path', 'file'),
        ('some/path/file.ext', 'some', 'path', 'file.ext'),
        ('repo', 'repo', None, None),
        ('repo/', 'repo', None, None),
        ('repo/.', 'repo', None, None),
        ('repo/./', 'repo', None, None),
        ('repo/./file', 'repo', None, 'file'),
        ('repo/file', 'repo', None, 'file'),
    ]
)
def test_split_component_path(
        component_path, x_repo, x_dir, x_file, nexus_mock_client):
    repository, directory, filename = nexus_mock_client.split_component_path(
        component_path)

    assert repository == x_repo
    assert directory == x_dir
    assert filename == x_file


@pytest.mark.parametrize(
    'component_path, x_error', [
        ('', 'does not contain a repository'),
        ('.', 'does not contain a repository'),
        ('./', 'does not contain a repository'),
    ]
)
def test_split_component_path_errors(
        component_path, x_error, nexus_mock_client):
    with pytest.raises(exception.NexusClientInvalidRepositoryPath) as e:
        nexus_mock_client.split_component_path(component_path)

    assert x_error in str(e.value)
