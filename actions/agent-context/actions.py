import os
import json
from typing import List, Optional
from sema4ai.actions import Response, action
from sema4ai.actions._action import get_current_requests_contexts
from pydantic import BaseModel, Field

class InvocationContext(BaseModel):
    workspace_id: Optional[str] = Field(default=None, description="Tenant ID (workspace)")
    agent_id: Optional[str] = Field(default=None, description="Agent ID")
    thread_id: Optional[str] = Field(default=None, description="Thread ID")
    invoked_on_behalf_of_user_id: Optional[str] = Field(default=None, description="User ID on whose behalf the action is invoked")
    action_invocation_id: Optional[str] = Field(default=None, description="Action invocation ID")

    class Config:
        extra = "allow"


@action
def return_all_env_variables() -> Response[List[str]]:
    """Returns all environment variables.

    Returns:
        List of environment variables
    """
    env_vars = []
    for e in os.environ:
        env_vars.append(f"{e} = {os.environ[e]}")
    return Response(result=env_vars)


@action
def get_context() -> Response[InvocationContext]:
    """This action is used to get the invocation context.

    Returns:
        information about the invocation context
    """
    current_requests_contexts = get_current_requests_contexts()
    invocation_context_raw = current_requests_contexts.invocation_context

    if invocation_context_raw and invocation_context_raw.value:
        invocation_context = _create_workroom_context(invocation_context_raw)
    else:
        invocation_context = _create_local_context(current_requests_contexts._request)
    return Response(result=invocation_context)

def _create_workroom_context(invocation_context_raw) -> InvocationContext:
    request_type = "WORK ROOM"
    workspace_id = invocation_context_raw.value.get('tenant_id', "UNKNOWN")
    agent_id = invocation_context_raw.value.get('agent_id', "UNKNOWN")
    thread_id = invocation_context_raw.value.get('thread_id', "UNKNOWN")
    action_invocation_id = invocation_context_raw.value.get('action_invocation_id', "UNKNOWN")
    invoked_on_behalf_of_user_id = invocation_context_raw.value.get('invoked_on_behalf_of_user_id', "UNKNOWN")
    return InvocationContext(
        workspace_id=workspace_id,
        agent_id=agent_id,
        thread_id=thread_id,
        action_invocation_id=action_invocation_id,
        invoked_on_behalf_of_user_id=invoked_on_behalf_of_user_id,
        request_type=request_type
    )

def _create_local_context(request) -> InvocationContext:
    request_type = "LOCAL"
    headers = request.headers
    config_file = os.path.expanduser('~/.sema4ai/sema4ai-studio/config.json')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            env_data = json.load(f)
            invoked_on_behalf_of_user_id = env_data.get('crUserEmail', "UNKNOWN")
    else:
        invoked_on_behalf_of_user_id = "UNKNOWN"
    workspace_id = "UNKNOWN"
    agent_id = headers.get('X-INVOKED_BY_ASSISTANT_ID', "UNKNOWN")
    thread_id = headers.get('X-INVOKED_FOR_THREAD_ID', "UNKNOWN")
    action_invocation_id = headers.get('X-ACTION_INVOCATION_ID', "UNKNOWN")
    return InvocationContext(
        workspace_id=workspace_id,
        agent_id=agent_id,
        thread_id=thread_id,
        action_invocation_id=action_invocation_id,
        invoked_on_behalf_of_user_id=invoked_on_behalf_of_user_id,
        request_type=request_type
    )