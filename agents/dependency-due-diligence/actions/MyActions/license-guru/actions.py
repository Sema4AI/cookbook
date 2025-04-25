from reports import generate_template, get_template_html_wrap, content_mock
from sema4ai.actions import action, Secret
from bs4 import BeautifulSoup
import anthropic
import requests
import json
from urllib.parse import urlparse


API_URL = "https://api.github.com"


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
    data = resp.json()
    last_versions = list(data["releases"])[-3:]
    releases = []
    try:
        for version in last_versions:
            releases.append(
                {version: data["releases"][version][0]["upload_time_iso_8601"]}
            )
    except KeyError:
        pass
    return json.dumps(
        {
            "license": data.get("info", {}).get("license"),
            "name": data.get("info", {}).get("name"),
            "package_url": data.get("info", {}).get("package_url"),
            "project_url": data.get("info", {}).get("project_url"),
            "project_urls": data.get("info", {}).get("project_urls"),
            "summary": data.get("info", {}).get("summary"),
            "version": data.get("info", {}).get("version"),
            "releases": releases,
        }
    )


@action
def parse_snyk(package_name: str) -> str:
    """
    Retrieves the HTML page on Snyk for the given package. It gives information
    regarding the security issues and CVEs for the package. It acts as a
    security scan

    Args:
        package_name (str): Name of the package to scan

    Returns:
        Returns the HTML page of the package on Snyk that needs to be parsed.
    """
    resp = requests.get(f"https://snyk.io/advisor/python/{package_name}/")
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text)
    content = soup.find_all("div", class_="package-container")
    if len(content) == 0:
        return "No content was found"
    return str(content[0])


@action
def get_repository(github_url: str) -> str:
    """Lookup repositories on github

    Args:
        github_url (str): repository URL

    Returns:
        str: json response of repository info.
    """
    parsed_url = urlparse(github_url)
    path_parts = parsed_url.path.strip("/").split("/")

    if len(path_parts) >= 2:
        owner = path_parts[0]
        repo = path_parts[1]
    else:
        return "URL is invalid"

    url = f"{API_URL}/repos/{owner}/{repo}"

    headers = {
        "Accept": "application/json",
    }

    resp = requests.get(url, headers=headers)
    data = resp.json()

    return json.dumps(data)


@action
def repository_releases(releases_url: str, page: int = 1, limit: int = 5) -> str:
    """Lookup repository releases

    Args:
        releases_url (str): Lookup repository releases
        page (int): Page number of the results
        limit (int): Number of results to return

    Returns:
        str: json response of repository release information.
    """

    url = releases_url.replace("{/id}", "")
    headers = {
        "Accept": "application/json",
    }

    resp = requests.get(url, headers=headers)
    data = resp.json()

    start_index = (page - 1) * limit
    return json.dumps(data[start_index : start_index + limit])


@action
def generate_report(context: str, secret_message: Secret) -> str:
    """
    Genereate a report about python dependencies based on github and synk parsing actions.

    Args:
        context (str): The context to use to generate the report. This contains report from github and pypi parsing actions
        secret_message (str): The secret message to use to generate the report.

    Returns:
        str: Returns an absolute path to a report html file on the local machine.
    """

    client = anthropic.Anthropic(
        api_key=secret_message.value,
    )

    template = get_template_html_wrap(
        generate_template(
            client,
            f"""Create the report based on the example <context>{context}</context>""",
            content_mock,
        )
    )

    wrapped = get_template_html_wrap(template)

    import datetime
    import os

    file_name = f"report-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
    folder = os.path.abspath("./tmp/")
    file_path = os.path.join(folder, file_name)

    os.makedirs("./tmp", exist_ok=True)

    with open(file_path, "w") as file:
        file.write(wrapped)

    return file_path