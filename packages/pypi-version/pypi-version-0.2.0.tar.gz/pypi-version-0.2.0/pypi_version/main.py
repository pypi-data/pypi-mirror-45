"""
Provide implementation of the PyPi version checking.
"""
import requests
from accessify import private

from pypi_version.cis import (
    CircleCi,
    TravisCi,
)
from pypi_version.constants import (
    FETCH_PYPI_PACKAGE_URL,
    HTTP_STATUS_OK,
)
from pypi_version.errors import (
    NOT_SUPPORTED_CONTINUOUS_INTEGRATION_ERROR_MESSAGE,
    NotSupportedContinuousIntegrationError,
)


class PypiPackageVersion:
    """
    Implementation of PyPi package version.
    """

    @staticmethod
    def does_exist(name, version):
        """
        Check if package with specified name and version already uploaded to the PyPi.

        Send request to the PyPi. If page is presented — package exist, else — does not exist.
        """
        response = requests.get(
            FETCH_PYPI_PACKAGE_URL.format(package_name=name, package_version=version),
        )

        if response.status_code == HTTP_STATUS_OK:
            return True

        return False


class PullRequest:
    """
    Implementation of pull request.
    """

    @private
    @staticmethod
    def get_ci(name):
        """
        Get continuous integration class with related data.
        """
        if name == TravisCi().name:
            return TravisCi()

        if name == CircleCi().name:
            return CircleCi()

        raise NotSupportedContinuousIntegrationError(
            NOT_SUPPORTED_CONTINUOUS_INTEGRATION_ERROR_MESSAGE.format(ci_name=name),
        )

    def is_for_check(self, ci_name, develop_branch, release_branch):
        """
        Check if current pull request matches pull request configurations in the configuration file.

        If current pull request configurations matches pull request configurations in the configuration file,
        then return true, else return false.
        """
        ci = self.get_ci(name=ci_name)

        if not ci.is_pull_request():
            return False

        if develop_branch != ci.pr_branch_from_name:
            return False

        if release_branch != ci.pr_branch_to_name:
            return False

        return True
