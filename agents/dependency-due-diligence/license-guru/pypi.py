from sema4ai.actions import action
import requests

@action
def get_metadata(pkg_name: str) -> str:
    """
    Retrieves the PyPi metadata for the given package.

    Args:
        pkg_name (str): Name of the package to scan

    Returns:
        Returns the JSON metadata of the package as a string.
    """
    resp = requests.get(f"https://pypi.org/pypi/{pkg_name}/json")
    resp.raise_for_status()
    return resp.json()


@action
def parse_pypi(pkg_name: str) -> str:
    """
    Retrieves the HTML page on PyPi for the given package.

    Args:
        pkg_name (str): Name of the package to scan

    Returns:
        Returns the HTML page of the package on PyPi that needs to be parsed.
    """
    resp = requests.get(f"https://pypi.org/project/{pkg_name}/")
    resp.raise_for_status()
    return resp.text


@action
def parse_snyk(pkg_name: str) -> str:
    """
    Retrieves the HTML page on Snyk for the given package. It gives information
    regarding the security issues and CVEs for the package. It acts as a
    security scan

    Args:
        pkg_name (str): Name of the package to scan

    Returns:
        Returns the HTML page of the package on PyPi that needs to be parsed.
    """
    resp = requests.get(f"https://pypi.org/project/{pkg_name}/")
    resp.raise_for_status()
    return resp.text