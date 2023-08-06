"""
Provide tests for PyPi version checking implementation.
"""
from pypi_version.constants import HTTP_STATUS_OK
from pypi_version.main import PypiPackageVersion


def test_pypi_package_version_exist(mocker, response):
    """
    Case: check if PyPi package version exists.
    Expect: true is returned.
    """
    response.status_code = HTTP_STATUS_OK

    mock_request_package = mocker.patch('requests.get')
    mock_request_package.return_value = response

    result = PypiPackageVersion.does_exist(name='Django', version='2.17.0')
    assert result is True


def test_pypi_package_version_does_not_exist(mocker, response):
    """
    Case: check if PyPi package version exists.
    Expect: false is returned.
    """
    response.status_code = None

    mock_request_package = mocker.patch('requests.get')
    mock_request_package.return_value = response

    result = PypiPackageVersion.does_exist(name='Django', version='14.1.5')
    assert result is False
