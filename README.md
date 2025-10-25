# foam-agent-mcp-core

Utilities for building MCP services around [Foam-Agent](https://github.com/OpenFOAM/foam-agent), including configuration loading, command construction, and process orchestration.

## Features

- Environment-driven configuration loader (`FoamAgentConfig`).
- Helpers for resolving relative paths and constructing shell commands.
- Process wrapper (`run_foam_agent_process`) that captures stdout/stderr for MCP responses.
- Log trimming utilities for user-facing output.

## Installation

```bash
pip install foam-agent-mcp-core
```

## Usage

```python
from foam_agent_mcp_core import load_config, build_shell_command, run_foam_agent_process
from pathlib import Path

config = load_config(Path("./extern/Foam-Agent"))
args, shell_command = build_shell_command(
    config,
    output_dir=Path("./job/output"),
    prompt_path=Path("./job/prompt.txt"),
    custom_mesh_path=None,
)

print("Executing", shell_command)
result = run_foam_agent_process(
    args,
    cwd=config.root,
    env={},
    timeout=3600,
)
print(result.stdout)
```

## Local development

Prerequisites:

- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv)

```bash
uv pip install --system -e '.[dev]'
uv run ruff check .
uv run pytest
```

## Repository structure

```
foam-agent-mcp-core/
├── src/foam_agent_mcp_core/   # Library source
├── tests/                     # Pytest regression tests
├── pyproject.toml             # Build metadata
└── .github/workflows/ci.yml   # Lint + test automation
```

## License

Released under the MIT License. See [LICENSE](LICENSE).
