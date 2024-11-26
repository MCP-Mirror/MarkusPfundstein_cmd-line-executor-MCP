
import json
import logging
from collections.abc import Sequence
from functools import lru_cache
from typing import Any

import subprocess
from dotenv import load_dotenv
from mcp.server import Server
import asyncio
from mcp.types import (

    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from pydantic import AnyUrl

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cmd-line-executor")

async def run_cmd_line(cmd: str, args: str | None) -> dict[str, Any]:

    cmd_list = [cmd]
    if args:
        cmd_list.append(args)
    
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd_list,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout_bytes, stderr_bytes = await process.communicate()
        
        stdout_lines = stdout_bytes.decode().strip().split('\n') if stdout_bytes else []
        stderr_lines = stderr_bytes.decode().strip().split('\n') if stderr_bytes else []
        
        stdout_lines = [line for line in stdout_lines if line]
        stderr_lines = [line for line in stderr_lines if line]
        
        return {
            "cmd": cmd,
            "args": args,
            "status_code": process.returncode or 0,
            "stdout": stdout_lines,
            "stderr": stderr_lines
        }
        
    except subprocess.SubprocessError as e:
        return {
            "cmd": cmd,
            "args": args,
            "status_code": 1,
            "stdout": [],
            "stderr": [str(e)]
        }
    except Exception as e:
        return {
            "cmd": cmd,
            "args": args,
            "status_code": 1,
            "stdout": [],
            "stderr": [f"Unexpected error: {str(e)}"]
        }

app = Server("cmd-line-executor")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available command line tools."""
    return [
        Tool(
            name="run_command",
            description="Runs a local command on the command line. Can take arguments.",
            inputSchema={
                "type": "object",
                "properties": {
                    "cmd": {
                        "type": "string",
                        "description": "The command to run."
                    },
                    "args": {
                        "type": "string",
                        "description": "The arguments to the command",
                    },
                },
                "required": ["cmd"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls for command line run."""
    if name != "run_command":
        raise ValueError(f"Unknown tool: {name}")

    if not isinstance(arguments, dict) or "cmd" not in arguments:
        raise ValueError("Invalid arguments")

    cmd : str = arguments["cmd"]
    args : str | None = None
    if "args" in arguments:
        args = arguments["args"]

    try:
        output = await run_cmd_line(cmd=cmd, args=args)

        return [
            TextContent(
                type="text",
                text=json.dumps(output, indent=2)
            )
        ]
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise RuntimeError(f"Error: {str(e)}")


async def main():
    # Import here to avoid issues with event loops
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )



