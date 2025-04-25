from sema4ai.actions import action, chat
from sema4ai_http import get

@action
def download_file_and_attach_to_chat(url: str, filename: str) -> str:
    """Download a file from a url and write it to a file

    Args:
        url: The url to download the file from
        filename: The name of the file to write to

    Returns:
        The full path to the file that was written
    """
    response = get(url)
    response.raise_for_status()
    chat.attach_file_content(filename, response.data)
    return f"File {filename} downloaded and attached to the chat"

@action
def get_file_from_chat(filename: str) -> str:
    """Get file from the chat

    Args:
        filename: The name of the file to get from the chat

    Returns:
        The full path to the file that was written. Show path to the user.
    """
    chat_file = chat.get_file(filename)
    return str(chat_file)
