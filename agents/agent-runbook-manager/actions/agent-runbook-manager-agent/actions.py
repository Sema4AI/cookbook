from io import BytesIO
from pathlib import Path
from typing import Literal, Optional, List

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from models import CommentList, File, FileList, Response
from sema4ai.actions import OAuth2Secret, action
import markdown
from bs4 import BeautifulSoup
import pandas as pd
import requests
from pydantic import BaseModel
from datetime import datetime

class AgentConfig(BaseModel):
    name: str
    description: str
    runbook: str

class AgentsInput(BaseModel):
    agents: List[AgentConfig]

load_dotenv(Path(__file__).absolute().parent / "devdata" / ".env")

EXPORT_MIMETYPE_MAP = {
    "application/vnd.google-apps.spreadsheet": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.google-apps.document": "text/plain",
}

def _build_drive_service(credentials: OAuth2Secret) -> Resource:
    creds = Credentials(token=credentials.access_token)
    return build("drive", "v3", credentials=creds)

def _build_docs_service(credentials: OAuth2Secret) -> Resource:
    creds = Credentials(token=credentials.access_token)
    return build("docs", "v1", credentials=creds)

def _get_runbook_by_name(service: Resource, name: str, folder_id: str) -> Optional[File]:
    response = service.files().list(q=f"name = '{name}' and '{folder_id}' in parents", fields="*").execute()
    if not response.get("files"):
        return None
    return File(**response["files"][0])

def _get_folder_id_by_name(service: Resource, folder_name: str) -> Optional[str]:
    response = service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'", fields="files(id)").execute()
    if not response.get("files"):
        return None
    return response["files"][0]["id"]

def _export_file_content(service: Resource, file_id: str, mime_type: str) -> BytesIO:
    request = service.files().export_media(fileId=file_id, mimeType=mime_type)
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    return fh

def _convert_markdown_to_html(markdown_content: str) -> str:
    html_content = markdown.markdown(markdown_content)
    return html_content

def _convert_html_to_google_docs_format(html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')
    return str(soup)

def _get_excel_content(file_content: BytesIO, worksheet: Optional[str] = None) -> str:
    if worksheet:
        df = pd.read_excel(file_content, sheet_name=worksheet)
    else:
        df = pd.read_excel(file_content)
    df_cleaned = df.rename(columns=lambda x: "" if x.startswith("Unnamed") else x)
    df_cleaned = df_cleaned.fillna("")
    return df_cleaned.to_string(index=False)

@action(is_consequential=True)
def create_runbook(
    google_credentials: OAuth2Secret[
        Literal["google"],
        list[Literal["https://www.googleapis.com/auth/documents"]],
    ],
    title: str,
    content: str = ""
) -> Response:
    """
    Creates a new runbook as a Google Doc with the specified title and content.

    Args:
        google_credentials: JSON containing Google OAuth2 credentials.
        title: Title of the Google Doc.
        content: Initial content of the Google Doc (in text or markdown).

    Returns:
        Response with the created document ID and URL or an error message.
    """
    service = _build_docs_service(google_credentials)
    document = {'title': title}
    try:
        doc = service.documents().create(body=document).execute()
        document_id = doc.get('documentId')
        if content:
            html_content = _convert_markdown_to_html(content)
            google_docs_content = _convert_html_to_google_docs_format(html_content)
            requests = [{'insertText': {'location': {'index': 1}, 'text': google_docs_content}}]
            service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        return Response(result=f"Runbook created: {document_id}: https://docs.google.com/document/d/{document_id}/edit")
    except HttpError as error:
        return Response(error=f"An error occurred: {error}")
    finally:
        service.close()

@action(is_consequential=True)
def update_runbook(
    google_credentials: OAuth2Secret[
        Literal["google"],
        list[Literal["https://www.googleapis.com/auth/documents"]],
    ],
    document_id: str,
    content: str
) -> Response:
    """
    Updates the content of an existing runbook, replacing the current content with the provided content.

    Args:
        google_credentials: JSON containing Google OAuth2 credentials.
        document_id: The ID of the Google Doc.
        content: The new content to replace the existing content (in text or markdown).

    Returns:
        Response with the updated document ID and a message or an error message.
    """
    service = _build_docs_service(google_credentials)
    try:
        requests = [{'deleteContentRange': {'range': {'startIndex': 1, 'endIndex': -1}}}]
        service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        html_content = _convert_markdown_to_html(content)
        google_docs_content = _convert_html_to_google_docs_format(html_content)
        requests = [{'insertText': {'location': {'index': 1}, 'text': google_docs_content}}]
        service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        return Response(result=f"Runbook updated: {document_id}")
    except HttpError as error:
        return Response(error=f"An error occurred: {error}")
    finally:
        service.close()

@action(is_consequential=True)
def get_runbook_content(
    google_credentials: OAuth2Secret[
        Literal["google"],
        list[Literal["https://www.googleapis.com/auth/drive.readonly"]],
    ],
    document_id: str
) -> Response:
    """
    Retrieves the content of a runbook.

    Args:
        google_credentials: JSON containing Google OAuth2 credentials.
        document_id: The ID of the Google Doc.

    Returns:
        Response with the runbook content or an error message.
    """
    service = _build_drive_service(google_credentials)
    try:
        file_content = _export_file_content(service, document_id, "text/plain")
        return Response(result=file_content.getvalue().decode("utf-8", errors="replace"))
    except HttpError as error:
        return Response(error=f"An error occurred: {error}")
    finally:
        service.close()

@action(is_consequential=False)
def get_runbook_version_history(
    google_credentials: OAuth2Secret[
        Literal["google"],
        list[Literal["https://www.googleapis.com/auth/drive.metadata.readonly"]],
    ],
    document_id: str
) -> Response:
    """
    Retrieves the version history of a runbook.

    Args:
        google_credentials: JSON containing Google OAuth2 credentials.
        document_id: The ID of the Google Doc.

    Returns:
        Response with the version history of the runbook or an error message.
    """
    service = _build_drive_service(google_credentials)
    try:
        versions = service.revisions().list(fileId=document_id).execute()
        return Response(result=str(versions.get('revisions', [])))
    except HttpError as error:
        return Response(error=f"An error occurred: {error}")
    finally:
        service.close()

@action(is_consequential=True)
def revert_runbook_to_version(
    google_credentials: OAuth2Secret[
        Literal["google"],
        list[Literal["https://www.googleapis.com/auth/drive"]],
    ],
    document_id: str,
    version_id: str
) -> Response:
    """
    Reverts a runbook to a specified previous version.

    Args:
        google_credentials: JSON containing Google OAuth2 credentials.
        document_id: The ID of the Google Doc.
        version_id: The ID of the version (revision) to revert to.

    Returns:
        Response with a message indicating the success or failure of the operation.
    """
    service = _build_drive_service(google_credentials)
    try:
        service.revisions().update(fileId=document_id, revisionId=version_id, body={"published": True}).execute()
        return Response(result=f"Runbook reverted to version: {version_id}")
    except HttpError as error:
        return Response(error=f"An error occurred: {error}")
    finally:
        service.close()

@action(is_consequential=True)
def sync_runbook(
    google_credentials: OAuth2Secret[
        Literal["google"],
        list[Literal["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive"]],
    ],
    document_id: str,
    new_content: str
) -> Response:
    """
    Synchronizes the runbook content with the latest updates.

    Args:
        google_credentials: JSON containing Google OAuth2 credentials.
        document_id: The ID of the Google Doc.
        new_content: The new content to update in the runbook (in text or markdown).

    Returns:
        Response with a message indicating the success or failure of the synchronization.
    """
    service_docs = _build_docs_service(google_credentials)
    service_drive = _build_drive_service(google_credentials)
    try:
        html_content = _convert_markdown_to_html(new_content)
        google_docs_content = _convert_html_to_google_docs_format(html_content)
        requests = [{'insertText': {'location': {'index': 1}, 'text': google_docs_content}}]
        service_docs.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        file_metadata = {'name': 'Updated Runbook'}
        service_drive.files().update(fileId=document_id, body=file_metadata).execute()
        return Response(result=f"Runbook synchronized and updated: {document_id}")
    except HttpError as error:
        return Response(error=f"An error occurred: {error}")
    finally:
        service_docs.close()
        service_drive.close()

@action(is_consequential=False)
def get_runbooks_by_query(
    google_credentials: OAuth2Secret[
        Literal["google"],
        list[
            Literal[
                "https://www.googleapis.com/auth/drive.readonly",
                "https://www.googleapis.com/auth/drive.metadata.readonly",
            ]
        ],
    ],
    query: str,
    folder_name: str
) -> Response[FileList]:
    """
    Get all runbooks from Google Drive that match the given query within a specific folder.

    Args:
        google_credentials: JSON containing Google OAuth2 credentials.
        query: Google Drive API V3 query string for search files in the format query_term operator values.
        folder_name: Name of the folder to search within.

    Returns:
        A list of runbooks or an error message if no runbooks were found.
    """
    service = _build_drive_service(google_credentials)
    try:
        folder_id = _get_folder_id_by_name(service, folder_name)
        if not folder_id:
            return Response(error=f"No folder named '{folder_name}' found")
        query = f"{query} and '{folder_id}' in parents"
        response = service.files().list(q=query, fields="*").execute()
        files = FileList(files=response.get("files", []))
        if not files.files:
            return Response(error=f"No runbooks were found for the query: {query}")
        return Response(result=files)
    except HttpError as error:
        return Response(error=f"An error occurred: {error}")
    finally:
        service.close()

@action(is_consequential=False)
def get_runbook_contents_by_name(
    google_credentials: OAuth2Secret[
        Literal["google"],
        list[Literal["https://www.googleapis.com/auth/drive.readonly"]],
    ],
    name: str,
    folder_name: str
) -> Response:
    """
    Get the runbook contents by name within a specific folder.

    Args:
        google_credentials: JSON containing Google OAuth2 credentials.
        name: Name of the runbook.
        folder_name: Name of the folder to search within.

    Returns:
        The runbook contents or an error message.
    """
    service = _build_drive_service(google_credentials)
    try:
        folder_id = _get_folder_id_by_name(service, folder_name)
        if not folder_id:
            return Response(error=f"No folder named '{folder_name}' found")
        query = f"name = '{name}' and '{folder_id}' in parents"
        response = service.files().list(q=query, fields="*").execute()
        if not response.get("files"):
            return Response(error=f"The runbook named '{name}' could not be found")
        file = File(**response["files"][0])
        file_content = _export_file_content(service, file.id, EXPORT_MIMETYPE_MAP[file.mimeType])
        if file.is_excel():
            return Response(result=_get_excel_content(file_content))
        return Response(result=file_content.getvalue().decode("utf-8", errors="replace"))
    except HttpError as error:
        return Response(error=f"An error occurred: {error}")
    finally:
        service.close()

@action(is_consequential=True)
def share_runbook(
    google_credentials: OAuth2Secret[
        Literal["google"],
        list[Literal["https://www.googleapis.com/auth/drive.file"]],
    ],
    name: str,
    role: str,
    email_address: str,
    folder_name: str
) -> Response:
    """
    Share a runbook with a specific email address within a specific folder.

    Args:
        google_credentials: JSON containing Google OAuth2 credentials.
        name: Name of the runbook to be shared.
        role: Assign a specific role. Possible options are: reader, writer, commenter, organizer, fileOrganizer.
        email_address: The email address of the user or group to share the runbook with.
        folder_name: Name of the folder to search within.

    Returns:
        Message indicating the success or failure of the operation.
    """
    service = _build_drive_service(google_credentials)
    permission = {"type": "user", "role": role, "emailAddress": email_address}
    try:
        folder_id = _get_folder_id_by_name(service, folder_name)
        if not folder_id:
            return Response(error=f"No folder named '{folder_name}' found")
        query = f"name = '{name}' and '{folder_id}' in parents"
        response = service.files().list(q=query, fields="*").execute()
        if not response.get("files"):
            return Response(error=f"The runbook named '{name}' could not be found")
        file = File(**response["files"][0])
        service.permissions().create(fileId=file.id, body=permission).execute()
        return Response(result=f"Permission {role} was granted. File link: {file.webViewLink}")
    except HttpError as e:
        return Response(error=f"Failed to share the runbook. Reason: {e.reason}")
    finally:
        service.close()

@action(is_consequential=False)
def list_runbook_comments(
    google_credentials: OAuth2Secret[
        Literal["google"],
        list[Literal["https://www.googleapis.com/auth/drive.readonly"]],
    ],
    name: str,
    folder_name: str
) -> Response[CommentList]:
    """
    List the comments on a specific runbook within a specific folder.

    Args:
        google_credentials: JSON containing Google OAuth2 credentials.
        name: Name of the runbook to read its associated comments.
        folder_name: Name of the folder to search within.

    Returns:
        List of comments associated with the runbook.
    """
    service = _build_drive_service(google_credentials)
    try:
        folder_id = _get_folder_id_by_name(service, folder_name)
        if not folder_id:
            return Response(error=f"No folder named '{folder_name}' found")
        query = f"name = '{name}' and '{folder_id}' in parents"
        response = service.files().list(q=query, fields="*").execute()
        if not response.get("files"):
            return Response(error=f"The runbook named '{name}' could not be found")
        file = File(**response["files"][0])
        comments_list = (
            service.comments()
            .list(fileId=file.id, fields="*")
            .execute()
            .get("comments", [])
        )
        return Response(result=CommentList(comments=comments_list))
    except HttpError as error:
        return Response(error=f"An error occurred: {error}")
    finally:
        service.close()

@action
def create_agents(input_data: AgentsInput) -> str:
    """Creates multiple agents with the given configurations and initializes a welcome thread for each

    Args:
        input_data (AgentsInput): An instance of AgentsInput containing agent configurations.

    Returns:
        str: A status message indicating the result of the API calls.
    """
    assistant_url = "http://localhost:8100/assistants"
    thread_url = "http://localhost:8100/threads"
    responses = []
    
    for agent in input_data.agents:
        runbook_separator = '\nYour instructions are:\n'
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        system_message = (
            f"You are an assistant with the following name: {agent.name}.\n"
            f"The current date and time is: {current_datetime}."
            f"{runbook_separator}{agent.runbook}"
        )

        body = {
            "name": agent.name,
            "config": {
                "configurable": {
                    "type": "agent",
                    "type==agent/agent_type": "GPT 4 Turbo",
                    "type==agent/interrupt_before_action": False,
                    "type==agent/retrieval_description": (
                        "Can be used to look up information that was uploaded to this assistant.\n"
                        "If the user is referencing particular files, that is often a good hint that information may be here.\n"
                        "If the user asks a vague question, they are likely meaning to look up info from this retriever, and you should call it!"
                    ),
                    "type==agent/system_message": system_message,
                    "type==agent/description": agent.description,
                    "type==agent/tools": []
                }
            }
        }

        try:
            response = requests.post(assistant_url, json=body)
            response.raise_for_status()
            assistant_id = response.json().get("assistant_id")

            thread_body = {
                "assistant_id": assistant_id,
                "name": "welcome",
                "starting_message": "Hi! How can I help you today?"
            }

            thread_response = requests.post(thread_url, json=thread_body, headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })
            thread_response.raise_for_status()

            responses.append({"name": agent.name, "status": "Created with welcome thread"})
        except requests.exceptions.HTTPError as http_err:
            responses.append({"name": agent.name, "status": f"HTTP error occurred: {http_err}"})
        except Exception as err:
            responses.append({"name": agent.name, "status": f"Other error occurred: {err}"})
    
    if all(response["status"] == "Created with welcome thread" for response in responses):
        return "All agents and their welcome threads created successfully."
    else:
        error_responses = [response for response in responses if response["status"] != "Created with welcome thread"]
        return f"Some agents or their welcome threads were not created successfully: {error_responses}"

        
        
