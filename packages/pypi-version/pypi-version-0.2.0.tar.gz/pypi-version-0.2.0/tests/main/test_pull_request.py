"""
Provide tests for pull request implementation.
"""
import os

import pytest

from pypi_version.errors import (
    NOT_SUPPORTED_CONTINUOUS_INTEGRATION_ERROR_MESSAGE,
    NotSupportedContinuousIntegrationError,
)
from pypi_version.main import PullRequest


def test_pull_request_is_for_check_not_supported_ci():
    """
    Case: check if pull request environment matches specified in the configuration file if CI isn't matched.
    Except: not supported continuous integration error.
    """
    expected_error_message = NOT_SUPPORTED_CONTINUOUS_INTEGRATION_ERROR_MESSAGE.format(ci_name='not-supported-ci')

    with pytest.raises(NotSupportedContinuousIntegrationError) as error:
        PullRequest().is_for_check(ci_name='not-supported-ci', develop_branch='develop', release_branch='master')

    assert expected_error_message == error.value.message


def test_pull_request_is_for_check_pull_request_build_travis():
    """
    Case: build a pull request on Travis-CI that matches pull request configurations in configuration file.
    Expect: build's environment variables data matches configurations in configuration file.
    """
    os.environ['TRAVIS_PULL_REQUEST_BRANCH'] = 'develop'
    os.environ['TRAVIS_BRANCH'] = 'master'

    result = PullRequest().is_for_check(ci_name='travis', develop_branch='develop', release_branch='master')
    assert result is True


def test_pull_request_is_for_check_branch_build_travis():
    """
    Case: build a branch (not a pull request) on Travis-CI.
    Expect: `TRAVIS_BRANCH` environment variable , so false is returned.
    """
    os.environ['TRAVIS_BRANCH'] = ''

    result = PullRequest().is_for_check(ci_name='travis', develop_branch='develop', release_branch='master')
    assert result is False


def test_pull_request_is_for_check_pull_request_build_with_unmatched_branch_from_configs_travis():
    """
    Case: build a pull request on Travis-CI that does not matches develop branch configurations in configuration file.
    Except: `TRAVIS_PULL_REQUEST_BRANCH` does not matched `develop_branch` in configuration file, so false is returned.
    """
    os.environ['TRAVIS_PULL_REQUEST_BRANCH'] = 'work'

    result = PullRequest().is_for_check(ci_name='travis', develop_branch='develop', release_branch='master')
    assert result is False


def test_pull_request_is_for_check_pull_request_build_with_unmatched_release_branch_configs_travis():
    """
    Case: build a pull request on Travis-CI that does not matches release branch configurations in configuration file.
    Except: `TRAVIS_BRANCH` does not matched `release_branch` in configuration file, so false is returned.
    """
    os.environ['TRAVIS_BRANCH'] = 'release'

    result = PullRequest().is_for_check(ci_name='travis', develop_branch='development', release_branch='master')
    assert result is False


def test_pull_request_is_for_check_pull_request_build_circle(mocker, response):
    """
    Case: build a pull request on Travis-CI that matches pull request configurations in configuration file.
    Expect: build's environment variables data matches configurations in configuration file.
    """
    os.environ['CIRCLE_BRANCH'] = 'develop'
    os.environ['CI_PULL_REQUEST'] = 'https://github.com/dmytrostriletskyi/test-pypi-version-circle-ci/pull/1'

    response._json = {
        'base': {
            'ref': 'master'
        }
    }

    mock_request_package = mocker.patch('requests.get')
    mock_request_package.return_value = response

    result = PullRequest().is_for_check(ci_name='circle', develop_branch='develop', release_branch='master')
    assert result is True


def test_pull_request_is_for_check_branch_build_circle():
    """
    Case: build a branch (not a pull request) on CircleCI.
    Expect: `CI_PULL_REQUEST` environment variable is empty, so false is returned.
    """
    os.environ['CI_PULL_REQUEST'] = ''

    result = PullRequest().is_for_check(ci_name='circle', develop_branch='develop', release_branch='master')
    assert result is False


def test_pull_request_is_for_check_pull_request_build_with_unmatched_branch_from_configs_circle():
    """
    Case: build a pull request on CircleCI that does not matches develop branch configurations in configuration file.
    Except: `CIRCLE_BRANCH` does not matched `develop_branch` in configuration file, so false is returned.
    """
    os.environ['CIRCLE_BRANCH'] = 'work'

    result = PullRequest().is_for_check(ci_name='circle', develop_branch='develop', release_branch='master')
    assert result is False


def test_pull_request_is_for_check_pull_request_build_with_unmatched_release_branch_configs_circle(mocker, response):
    """
    Case: build a pull request on CircleCI that does not matches release branch configurations in configuration file.
    Except: pull request branch to does not matched `release_branch` in configuration file, so false is returned.
    """
    os.environ['CIRCLE_BRANCH'] = 'develop'
    os.environ['CI_PULL_REQUEST'] = 'https://github.com/dmytrostriletskyi/test-pypi-version-circle-ci/pull/1'

    response._json = {
        'base': {
            'ref': 'release'
        }
    }

    mock_request_package = mocker.patch('requests.get')
    mock_request_package.return_value = response

    result = PullRequest().is_for_check(ci_name='travis', develop_branch='development', release_branch='master')
    assert result is False
