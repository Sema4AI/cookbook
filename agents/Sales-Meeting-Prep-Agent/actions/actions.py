"""
A bare-bone AI Action template

Please check out the base guidance on AI Actions in our main repository readme:
https://github.com/sema4ai/actions/blob/master/README.md

"""

from sema4ai.actions import action
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from typing import List, Dict, Any
import json
import ast

@action
def write_to_json(file_path: str, data: str) -> bool:
    """
    Enables the action to write to a json file.

    Args:
        file_path(str): Creates a new file.
        data(str): The data to be written (as a string).

    Returns:
        A boolean indication if the write worked
    """
    try:
        data = ast.literal_eval(data)
        with open(file_path, "w+") as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(f"Error, {e}")
        return False
    
@action
def read_from_file(file_path: str) -> str:
    """
    Action to read from a file when given its file path.

    Args:
        file_path(str): The file path which points to the file to read.
    
    Returns:
        A string that is the contents of the file.
    """
    data = " "
    with open(file_path, "r") as f:
        data = f.read()
    return data
    
@action
def load_json(file_path: str) -> str:
    """
    Loads data from a JSON file from the given path.

    Args:
        file_path(str): The file path pointing to the JSON file.
    
    Returns:
        A tring containing the contents of the JSON file.
    """
    data = {}
    with open(file_path, "r") as f:
        data = json.load(f)
    data = str(data)
    return data
