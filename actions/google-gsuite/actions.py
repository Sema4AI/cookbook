"""
A bare-bone AI Action template

Please check out the base guidance on AI Actions in our main repository readme:
https://github.com/sema4ai/actions/blob/master/README.md

"""

from dotenv import load_dotenv
from pathlib import Path
from typing import Literal
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from _common import generate_password, create_body_message

from sema4ai.actions import action, OAuth2Secret, Response, ActionError

load_dotenv(Path(__file__).absolute().parent / "devdata" / ".env")


@action
def create_gsuite_user(
    primary_email: str,
    given_name: str,
    family_name: str,
    token: OAuth2Secret[
        Literal["google"],
        list[Literal["https://www.googleapis.com/auth/admin.directory.user"]],
    ],
) -> Response:
    """
    Action creates a company GSuite email to new employee

    Arguments:
        primary_email: email address to new employee
        given_name: employee's first name
        family_name: employee's last name
        token: 0auth2token for the user

    Returns:
        Returns message to be used as an email body
    """
    creds = Credentials(token=token.access_token)
    service = build("admin", "directory_v1", credentials=creds)

    # User details
    password = generate_password()
    template_body = create_body_message(primary_email, password)
    user_info = {
        "primaryEmail": primary_email,
        "name": {"givenName": given_name, "familyName": family_name},
        "password": password,
        "changePasswordAtNextLogin": True,
    }

    # Creating the new user
    try:
        service.users().insert(body=user_info).execute()
        result = f'Email body message is: "{template_body}"'
        print(result)
        return Response(result=result)
    except Exception as e:
        error_text = f"An error occurred: {e}"
        print(error_text)
        raise ActionError(error_text)
