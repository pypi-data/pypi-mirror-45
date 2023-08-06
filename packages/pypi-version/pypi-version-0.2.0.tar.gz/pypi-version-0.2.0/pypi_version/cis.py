"""
Provide implementation of continuous integration services.
"""
import os

import requests

from pypi_version.constants import FETCH_GITHUB_PULL_REQUEST_INFO_URL


class TravisCi:
    """
    Travis continuous integration class with related data.
    """

    @property
    def name(self):
        """
        Get lowercase name of the continuous integration service.
        """
        return 'travis'

    @property
    def pr_branch_from_name(self):
        """
        Get the pull request's branch from name.
        """
        return os.environ.get('TRAVIS_PULL_REQUEST_BRANCH')

    @property
    def pr_branch_to_name(self):
        """
        Get the pull request's branch to name.
        """
        return os.environ.get('TRAVIS_BRANCH')

    @staticmethod
    def is_pull_request():
        """
        Check if build on pull request build.
        """
        if not os.environ.get('TRAVIS_BRANCH'):
            return False

        return True


class CircleCi:
    """
    Circle continuous integration class with related data.
    """

    @property
    def name(self):
        """
        Get lowercase name of the continuous integration service.
        """
        return 'circle'

    @property
    def pr_branch_from_name(self):
        """
        Get the pull request's branch from name.
        """
        return os.environ.get('CIRCLE_BRANCH')

    @property
    def pr_branch_to_name(self):
        """
        Get the pull request's branch to name.
        """
        pull_request_url = os.environ.get('CI_PULL_REQUEST')
        pull_request_number = pull_request_url.split('/')[-1]

        project_owner_username = os.environ.get('CIRCLE_PROJECT_USERNAME')
        project_name = os.environ.get('CIRCLE_PROJECT_REPONAME')

        response = requests.get(
            FETCH_GITHUB_PULL_REQUEST_INFO_URL.format(
                project_owner_username=project_owner_username,
                project_name=project_name,
                pull_request_number=pull_request_number,
            ),
        )

        return response.json().get('base').get('ref')

    @staticmethod
    def is_pull_request():
        """
        Check if build on pull request build.
        """
        if not os.environ.get('CI_PULL_REQUEST'):
            return False

        return True
