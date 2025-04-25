from robocorp.tasks import task
from robocorp import vault, workitems
from typing import Optional, List, Dict
from sema4ai_http import get, post

DEFAULT_CONVERSATION_NAME = "Test Conversation"
DEFAULT_PROMPT = "Download https://cdn.robocorp.com/security/security-and-data-protection-whitepaper.pdf and attach it to fileswith name whitepaper.pdf"


class Sema4APIClient:
    def __init__(self, agent_id: str = None):
        secrets = vault.get_secret("agent_api")
        self.agent_id = agent_id if agent_id else secrets["AGENT_ID"]
        self.api_key = secrets["AGENT_API_KEY"]
        self.endpoint_url = secrets["AGENT_ENDPOINT_URL"].rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _make_get(self, endpoint: str) -> dict:
        url = f"{self.endpoint_url}{endpoint}"
        response = get(url, headers=self.headers)
        return response.json()

    def _make_post(self, endpoint: str, data: Optional[dict] = None) -> dict:
        url = f"{self.endpoint_url}{endpoint}"
        response = post(
            url,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()


    def get_agents(self) -> List[Dict]:
        """
        Get a list of all available agents
        Returns a list of agent objects
        """
        return self._make_get("/api/v1/agents")

    def create_conversation(self, name: str = "New Conversation") -> str:
        """
        Create a new conversation for the specified agent
        Returns the conversation ID
        """
        endpoint = f"/api/v1/agents/{self.agent_id}/conversations"
        data = {"name": name}
        response = self._make_post(endpoint, data)
        return response.get("id")

    def send_message(self, conversation_id: str, message: str) -> dict:
        """
        Send a message to an existing conversation
        Returns the message response
        """
        endpoint = f"/api/v1/agents/{self.agent_id}/conversations/{conversation_id}/messages"
        data = {"content": message}
        return self._make_post(endpoint, data)

@task
def list_available_agents():
    client = Sema4APIClient()

    # Get list of all agents
    agents = client.get_agents()

    print("Available agents:")
    print(f"\tnext = {agents['next']}, has_more = {agents['has_more']}")
    for agent in agents['data']:
        print(agent)


@task
def create_agent_conversation():
    agent_id, conversation_name, prompt = _get_agent_variables(workitems.inputs.current.payload)
    client = Sema4APIClient(agent_id)
    conversation_id = client.create_conversation(conversation_name)
    response = client.send_message(conversation_id, prompt)
    _print_conversation_messages(response)


def _get_agent_variables(item_payload):
    print(f"Input workitem payload: {item_payload}")
    agent_id = item_payload['agent_id'] if item_payload and "agent_id" in item_payload.keys() else None
    agent_name = item_payload['agent_name'] if item_payload and "agent_name" in item_payload.keys() else None
    if agent_name:
        agent_id = _get_agent_id(agent_name)
    conversation_name = item_payload['conversation_name'] if item_payload and "conversation_name" in item_payload.keys() else DEFAULT_CONVERSATION_NAME
    prompt = item_payload['prompt'] if item_payload and "prompt" in item_payload.keys() else DEFAULT_PROMPT
    return agent_id, conversation_name, prompt

def _print_conversation_messages(response):
    print("Messages in the conversation:")
    for msg in response['messages']:
        msg_type = msg['type']
        content = msg['content']
        if msg_type == 'action_request':
            content = ','.join([act['name'] for act in msg['action_calls']])
        elif msg_type == 'action_response':
            content = msg['status']
        print(f"\ttype: {msg_type}, content: {content}")

def _get_agent_id(agent_name):
    client = Sema4APIClient()
    agents = client.get_agents()
    for agent in agents['data']:
        if agent['name'].lower() == agent_name.lower():
            return agent['id']
    raise ValueError(f"Agent with name '{agent_name}' not found")
