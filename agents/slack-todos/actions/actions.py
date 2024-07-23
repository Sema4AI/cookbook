"""
A bare-bone AI Action template

Please check out the base guidance on AI Actions in our main repository readme:
https://github.com/sema4ai/actions/blob/master/README.md

"""

import os
from pathlib import Path
from sema4ai.actions import action
from todoist_api_python.api import TodoistAPI
from sema4ai.actions import Secret
from dotenv import load_dotenv

import json

load_dotenv(Path(__file__).absolute().parent / "devdata" / ".env")
DEV_TODOIST_ACCESS_TOKEN = Secret.model_validate(os.getenv("DEV_TODOIST_ACCESS_TOKEN", ""))


@action
def get_todoist_active_tasks(access_token: Secret = DEV_TODOIST_ACCESS_TOKEN) -> str:
    """
    Todoist action get list of active tasks

    Args:
        access_token: The access token for the Todoist API
    
    Returns:
        an array of JSON data that list the tasks and its details.
    """

    api = TodoistAPI(access_token.value)

    try:
        tasks = api.get_tasks()
        print(tasks)
    except Exception as error:
        print(error)
    return json.dumps(tasks, default=vars)
