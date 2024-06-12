"""
A bare-bone AI Action template

Please check out the base guidance on AI Actions in our main repository readme:
https://github.com/sema4ai/actions/blob/master/README.md

"""

from dotenv import load_dotenv
import os
from pathlib import Path
import requests

from sema4ai.actions import action, Response, Secret

load_dotenv(Path(__file__).absolute().parent / "devdata" / ".env")


@action
def create_hibob(
    first_name: str,
    surname: str,
    email: str,
    site: str,
    start_date: str,
    department: str,
    api_key: Secret = Secret.model_validate(os.getenv("HIBOB_API_KEY", "")),
) -> Response:
    """
    Creates a new employee in the Hibob system.

    Args:
        first_name: Employee's first name.
        surname: Employee's surname.
        email: Employee's email address.
        site: Employee's site
        start_date: Employee's start date e.g. 2024-06-22
        department: Employee's job department
        api_key: API key for Hibob authentication.

    Returns:
        Result of the action
    """
    url = "https://api.hibob.com/v1/people"
    headers = {
        "Authorization": f"Basic {api_key.value}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "firstName": first_name,
        "surname": surname,
        "email": email,
        "work": {
            "site": site,
            "startDate": start_date,
            "department": department,
        },
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        error_message = response.json().get("error", "Unknown error")
        return Response(result="error", error_message=error_message)
    return Response(result="ok")
