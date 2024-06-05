from sema4ai.actions import action
from bs4 import BeautifulSoup
import requests
import json

@action
def get_metadata(package_name: str) -> str:
    """
    Retrieves the PyPi metadata for the given package.

    Args:
        package_name (str): Name of the package to scan

    Returns:
        Returns the JSON metadata of the package as a string.
    """
    resp = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    resp.raise_for_status()
    return json.dumps(resp.json())


@action
def parse_snyk(package_name: str) -> str:
    """
    Retrieves the HTML page on Snyk for the given package. It gives information
    regarding the security issues and CVEs for the package. It acts as a
    security scan

    Args:
        package_name (str): Name of the package to scan

    Returns:
        Returns the HTML page of the package on PyPi that needs to be parsed.
    """
    resp = requests.get(f"https://snyk.io/advisor/python/{package_name}/")
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text)
    content = soup.find_all("div", class_="package-container")
    if len(content) == 0:
        return "No content was found"
    return content[0]