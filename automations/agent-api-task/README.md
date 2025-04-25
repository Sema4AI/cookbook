# Triggering Sema4.ai Agent from Robocorp Control Room

Task package contains two tasks.

First task `list_available_agents` which lists all agents that are available from given API endpoint with given API key.

Second task `create_agent_conversation` creates new conversation with selected agent and prompts it and gets the response.

Secrets that in this example are set in the Robocorp Vault `agent_api`:
- **AGENT_ID** (use `list_available_agents` or get this Sema4.ai Work Room)
- **AGENT_API_KEY** (get this from Sema4.ai Control Room)
- **AGENT_ENDPOINT_URL** (get this from Sema4.ai Control Room)

## Custom variables via input work item

For `create_agent_conversation` task. All of these are optional - task works with empty work item (provided that your agent can understand the default prompt).

- **agent_name** (will search for agent with this name and use it if found, error otherwise)
- **agent_id** (default. **AGENT_ID** from Robocorp Vault)
- **conversation_name** (default. `Test Conversation`)
- **prompt** (default. `Download https://cdn.robocorp.com/security/security-and-data-protection-whitepaper.pdf and attach it to files with name whitepaper.pdf`)

### Links
- [Sema4.ai Agent API](https://sema4.ai/docs/agent-api)
- [Robocorp Automation](https://sema4.ai/docs/automation/python/robocorp)
