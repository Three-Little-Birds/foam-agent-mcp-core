# foam-agent-mcp-core

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-brightgreen.svg)](pyproject.toml)

Utilities for wiring [Foam-Agent](https://github.com/OpenFOAM/foam-agent) into [Model Context Protocol](https://modelcontextprotocol.io/) services. The helpers manage configuration, command construction, subprocess execution, and log trimming so MCP servers can focus on scenario logic.

## Features

- Environment-driven configuration loader (`FoamAgentConfig`) with support for localized overrides.
- Utilities for resolving relative paths and building Foam-Agent CLI invocations.
- Testable process wrapper (`run_foam_agent_process`) that captures stdout/stderr for MCP responses.
- Log trimming helpers for structured tool outputs.

## Installation

Install directly from GitHub:

```bash
pip install "git+ssh://git@github.com/yevheniikravchuk/foam-agent-mcp-core.git"
```

or add to `pyproject.toml`:

```toml
foam-agent-mcp-core = { git = "ssh://git@github.com/yevheniikravchuk/foam-agent-mcp-core.git" }
```

## Usage

```python
from pathlib import Path

from foam_agent_mcp_core import (
    load_config,
    build_shell_command,
    run_foam_agent_process,
)

config = load_config(Path("./extern/Foam-Agent"))
args, shell_command = build_shell_command(
    config,
    output_dir=Path("./job/output"),
    prompt_path=Path("./job/prompt.txt"),
    custom_mesh_path=None,
)

print("Executing", shell_command)
result = run_foam_agent_process(args, cwd=config.root, env={}, timeout=3600)
print(result.stdout)
```

### Quickstart (MCP integration)

```python
from mcp.server.fastmcp import FastMCP
from foam_agent_mcp_core import load_config, build_shell_command, run_foam_agent_process

mcp = FastMCP("foam-agent-mcp", "Foam-Agent CFD automation")
CONFIG = load_config(Path("./extern/Foam-Agent"))

@mcp.tool()
def run(request):
    args, command = build_shell_command(
        CONFIG,
        output_dir=Path("./job/output"),
        prompt_path=Path("./job/prompt.txt"),
        custom_mesh_path=None,
    )
    result = run_foam_agent_process(args, cwd=CONFIG.root, env={}, timeout=request.get("timeout"))
    return {"command": command, "stdout": result.stdout}

if __name__ == "__main__":
    mcp.run()
```

Run the tool locally:

```bash
uv run mcp dev examples/foam_agent_tool.py
```

## Local development

Prerequisites:

- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv)

```bash
uv pip install --system -e ".[dev]"
uv run ruff check .
uv run pytest
```

## Repository structure

```
foam-agent-mcp-core/
├── src/foam_agent_mcp_core/
├── tests/
├── pyproject.toml
└── .github/workflows/ci.yml
```

## License

Released under the MIT License. See [LICENSE](LICENSE).

## Support

Open an issue or submit a pull request with improvements. Please include tests and documentation updates where appropriate.
