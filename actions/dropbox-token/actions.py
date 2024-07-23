"""
Collection of actions for accessing and interacting with Dropbox resources.

This package uses tokens for authentication.
"""

import requests
import json
import re
from io import BufferedReader
from sema4ai.actions import action, Secret

DELETE_URL = "https://api.dropboxapi.com/2/files/delete_v2"
DIRECTORY_CONTENTS_URL = "https://api.dropboxapi.com/2/files/list_folder"
DIRECTORY_CREATE_URL = "https://api.dropboxapi.com/2/files/create_folder_v2"
FILE_CONTENTS_READ_URL = "https://content.dropboxapi.com/2/files/download"
FILE_CONTENTS_WRITE_URL = "https://content.dropboxapi.com/2/files/upload"

DOWNLOAD_CHUNK_SIZE = 8192
UPLOAD_CHUNK_SIZE = 1024

def entry_to_file_item(
    entry: dict[str, str]
) -> dict[str, str]:
    return {
        "file_name": entry["name"],
        "full_path": entry["path_display"],
        "type": "directory" if entry[".tag"] == "folder" else "file",
        "size": entry["size"] if "size" in entry else 0
    }

def read_chunks(file_object: BufferedReader, chunk_size: int):
    while not file_object.closed:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def url_safe_range_replace(match) -> str:
    char = match.group()

    encoded = f"000{hex(ord(char[0]))}"

    return encoded[-4:]

def url_safe_json_dumps(
    item: dict
) -> str:
    output = json.dumps(item, separators=(',', ':'))

    return re.sub(r"[\u007f-\uffff]", url_safe_range_replace, output)

###########
# ACTIONS #
###########

@action
def create_directory(
    dropbox_token: Secret,
    remote_path: str
) -> str:
    """
    Create a remote directory/path on a Dropbox account.

    Args:
        dropbox_token: The access token for an account.
        remote_path: The remote directory path to create.

    Returns:
        The created path.
    """

    response = requests.post(
        DIRECTORY_CREATE_URL,
        headers = {
            "Authorization": f"Bearer {dropbox_token.value}",
            "Content-Type": "application/json"
        },
        data = json.dumps({
            "path": remote_path,
            "autorename": False
        })
    )
    response.raise_for_status()

    return remote_path

@action
def delete_file(
    dropbox_token: Secret,
    remote_path: str
) -> str:
    """
    Delete a remote directory/file on a Dropbox account.

    Args:
        dropbox_token: The access token for an account.
        remote_path: The remote path to delete.

    Returns:
        The deleted path.
    """

    response = requests.post(
        DELETE_URL,
        headers = {
            "Authorization": f"Bearer {dropbox_token.value}",
            "Content-Type": "application/json"
        },
        data = json.dumps({
            "path": remote_path
        })
    )
    response.raise_for_status()

    return remote_path

@action
def download_file(
    dropbox_token: Secret,
    remote_path: str,
    local_path: str
) -> str:
    """
    Download a remote file from a Dropbox account.

    Args:
        dropbox_token: The access token for an account.
        remote_path: The remote file path.
        local_path: The local file path to download to.

    Returns:
        The downloaded location of the file.
    """

    with requests.get(
        FILE_CONTENTS_READ_URL,
        headers = {
            "Authorization": f"Bearer {dropbox_token.value}",
            "Dropbox-API-Arg": url_safe_json_dumps({
                "path": remote_path
            })
        },
        stream = True
    ) as response:
        response.raise_for_status()

        with open(local_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                file.write(chunk)

    return local_path

@action
def get_file_contents(
    dropbox_token: Secret,
    remote_path: str
) -> str:
    """
    Get the file contents of a text-based file on a Dropbox account.

    Args:
        dropbox_token: The access token for an account.
        remote_path: The remote file path.

    Returns:
        The text contents of the remote file.
    """

    response = requests.get(
        FILE_CONTENTS_READ_URL,
        headers = {
            "Authorization": f"Bearer {dropbox_token.value}",
            "Content-Type": "text/plain",
            "Dropbox-API-Arg": url_safe_json_dumps({
                "path": remote_path
            })
        }
    )
    response.raise_for_status()

    return response.text

@action
def list_files(
    dropbox_token: Secret,
    remote_path: str
) -> str:
    """
    List remote files and folders on a Dropbox account.

    Args:
        dropbox_token: The access token for an account.
        remote_path: The remote directory path to request against.

    Returns:
        A list of files and folders.
    """

    response = requests.post(
        DIRECTORY_CONTENTS_URL,
        headers = {
            "Authorization": f"Bearer {dropbox_token.value}",
            "Content-Type": "application/json"
        },
        data = json.dumps({
            "path": "" if remote_path == "/" else remote_path,
            "recursive": False,
            "limit": 2000,
            "include_media_info": False,
            "include_deleted": False,
            "include_has_explicit_shared_members": False,
            "include_mounted_folders": True
        })
    )
    response.raise_for_status()

    result = response.json()

    files = list(map(entry_to_file_item, result["entries"]))

    return json.dumps(files, separators=(',', ':'))

@action
def put_file_contents(
    dropbox_token: Secret,
    remote_path: str,
    file_contents: str
) -> str:
    """
    Put file contents at a remote path on a Dropbox account.

    Args:
        dropbox_token: The access token for an account.
        remote_path: The remote file path.
        file_contents: The file contents to write.

    Returns:
        The remote path written to.
    """

    response = requests.post(
        FILE_CONTENTS_WRITE_URL,
        headers = {
            "Authorization": f"Bearer {dropbox_token.value}",
            "Content-Type": "application/octet-stream"
        },
        params = {
            "arg": url_safe_json_dumps({
                "path": remote_path,
                "mode": "overwrite"
            })
        },
        data = file_contents
    )
    response.raise_for_status()

    return remote_path

@action
def upload_file(
    dropbox_token: Secret,
    remote_path: str,
    local_file: str
) -> str:
    """
    Upload a local file to a Dropbox account.

    Args:
        dropbox_token: The access token for an account.
        remote_path: The remote file path.
        local_file: The local file path to upload.

    Returns:
        The remote path uploaded to.
    """

    with open(local_file, "br") as file:
        with requests.post(
            FILE_CONTENTS_WRITE_URL,
            headers = {
                "Authorization": f"Bearer {dropbox_token.value}",
                "Content-Type": "application/octet-stream"
            },
            params = {
                "arg": url_safe_json_dumps({
                    "path": remote_path,
                    "mode": "overwrite"
                })
            },
            data = read_chunks(file, UPLOAD_CHUNK_SIZE)
        ) as response:
            response.raise_for_status()

    return remote_path
