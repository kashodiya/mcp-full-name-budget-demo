

## Run MCP server
uv run main.py

## How to run Inspector
npx @modelcontextprotocol/inspector
- http://127.0.0.1:6274
- Transport: SSE
- URL: http://0.0.0.0:8080/sse
- Click Tools -> List Tools
- See: History

## Use the server
- Open VSCode
- Open Copilot
- Select Agent (under the text/question box)
- Shift+Cmd+P => MCP Add Server => Add Server => HTTP
- Enter http://0.0.0.0:8080/sse
- Start connecting to the server, if not started
    - Shift+Cmd+P => MCP List Server => Select the one added => Start
- Ask question 
    - Get my full name
- Ask question  
Answer following questions based on the budget data:
- What are the unique business lines?
- What is total budget of 2024?
- What is total budget?
- What is the budget of BL789

