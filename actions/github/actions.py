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
        str: page or section html.
    """

    url = f"{API_URL}/search/repositories?q={query}&page={page}&limit={limit}"
    headers = {
        "Accept": "application/json",
    }

    resp = requests.get(url, headers=headers)
    data = resp.json()

    return json.dumps(data.get('items'))

@action
def repository_releases(releases_url: str, page: int = 1, limit: int = 5) -> str:
    """Lookup repository releases

    Args:
        releases_url (str): Lookup repository releases
        page (int): Page number of the results
        limit (int): Number of results to return

    Returns:
        str: page or section html.
    """

    url = releases_url.replace("{/id}", "")
    headers = {
        "Accept": "application/json",
    }

    resp = requests.get(url, headers=headers)
    data = resp.json()

    start_index = (page - 1) * limit
    return json.dumps(data[start_index:start_index + limit])
