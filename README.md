# cmd-line-executor MCP server

Example MCP server to call command line apps

## Components

### Tools

The server implements one tool:
- run_command: Runs a command line comment
  - Takes "cmd" and "args" as string arguments
  - Runs the command and returns stdout, stderr, status_code, etc.

## Configuration


## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "cmd-line-executor": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/$(whoami)/experiments/claude-mvp/cmd-line-executor",
        "run",
        "cmd-line-executor"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  ```
  "mcpServers": {
    "cmd-line-executor": {
      "command": "uvx",
      "args": [
        "cmd-line-executor"
      ]
    }
  }
  ```
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /Users/markus/experiments/claude-mvp/cmd-line-executor run cmd-line-executor
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.
