"""
Provide constants for PyPi version checking.
"""
PYPI_VERSION_CHECKING_PASSED_SYS_CODE = 0
PYPI_VERSION_CHECKING_FAILED_SYS_CODE = -1

PYPI_VERSION_CONFIG_FILE_NAME = 'pypi-version'
FETCH_PYPI_PACKAGE_URL = 'https://pypi.org/project/{package_name}/{package_version}/'
FETCH_GITHUB_PULL_REQUEST_INFO_URL = \
    'https://api.github.com/repos/{project_owner_username}/{project_name}/pulls/{pull_request_number}'

HTTP_STATUS_OK = 200
HTTP_STATUS_NOT_FOUND = 404
