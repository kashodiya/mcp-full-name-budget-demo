from typing import Any
# import httpx
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
import uvicorn
import json
from typing import List, TypedDict


# Initialize FastMCP server for Weather tools (SSE)
mcp = FastMCP("mcp-sse-1")

@mcp.tool()
def get_first_name() -> str:
    """Get first name.
    """
    return "Kaushik"

@mcp.tool()
def get_last_name() -> str:
    """Get last name.
    """
    return "Ashodiya"

@mcp.tool()
def get_full_name(first_name: str, last_name: str) -> str:
    """Get full name from a given first and last name.

    Args:
        first_name: First name
        last_name: Last name
    """
    return f"{first_name} {last_name}"

class BudgetRecord(TypedDict):
    year: int
    month: str
    budget_amount: float
    business_line: str

@mcp.tool()
def get_budget() -> List[BudgetRecord]:
    """Get budget data as a list of records from a JSON file.
    
    Returns:
        List[BudgetRecord]: A list of budget records read from the JSON file.
    """
    
    # Path to the JSON file
    json_file_path = 'budget_data.json'
    
    # Read data from the JSON file
    with open(json_file_path, 'r') as file:
        budget_data = json.load(file)
    
    return budget_data



def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can server the provied mcp server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )


if __name__ == "__main__":
    mcp_server = mcp._mcp_server  # noqa: WPS437

    import argparse
    
    parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port to listen on')
    args = parser.parse_args()

    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)

    uvicorn.run(starlette_app, host=args.host, port=args.port)
