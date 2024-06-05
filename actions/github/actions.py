import requests
import json

from sema4ai.actions import action

API_URL = "https://api.github.com"

@action
def search_repository(query: str, page: int = 1, limit: int = 1) -> str:
    """Lookup repositories on github

    Args:
        query (str): Search query for repository
        page (int): Page number of the results
        limit (int): Number of results to return

    Returns:
        str: json list of repositories responses.
    """

    url = f"{API_URL}/search/repositories?q={query}&page={page}&limit={limit}"
    headers = {
        "Accept": "application/json",
    }

    resp = requests.get(url, headers=headers)
    data = resp.json()

    return json.dumps(data.get('items'))

@action
def get_repository(repo: str, owner: str = "") -> str:
    """Lookup repositories on github

    Args:
        repo (str): repo name, can be full or partial if owner specified
        owner (int): optional owner of repository

    Returns:
        str: json response of repository info.
    """

    if owner != "":
        url = f"{API_URL}/repos/{owner}/{repo}"
    else:
        url = f"{API_URL}/repos/{repo}"

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
    return json.dumps(data[start_index:start_index + limit])
