# foam-agent-mcp-core · Step-by-Step Helper for Foam-Agent MCP Services

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-brightgreen.svg)](pyproject.toml)
[![CI](https://github.com/yevheniikravchuk/foam-agent-mcp-core/actions/workflows/ci.yml/badge.svg)](https://github.com/yevheniikravchuk/foam-agent-mcp-core/actions/workflows/ci.yml)

This package documents how to integrate [Foam-Agent](https://github.com/csml-rpi/Foam-Agent) with Model Context Protocol services. It handles configuration discovery, command construction, and log trimming—giving students and automation engineers a head start on CFD orchestration.

## What you will build

1. Load Foam-Agent configuration from environment variables or local overrides.
2. Construct the exact shell command Foam-Agent expects and run it safely.
3. Return a trimmed archive (mesh, forces, logs) suitable for MCP responses.

## Step 1 – Install the helper

```bash
uv pip install "git+https://github.com/yevheniikravchuk/foam-agent-mcp-core.git"
```

## Step 2 – Discover configuration

```python
from pathlib import Path
from foam_agent_mcp_core import load_config

config = load_config(Path("~/Foam-Agent").expanduser())
print(config.root)
print(config.python)
```

`FoamAgentConfig` reads environment overrides such as `FOAM_AGENT_ROOT`, `FOAM_AGENT_ACTIVATE`, and `FOAM_AGENT_OPENFOAM_PATH`, making deployments reproducible.

## Step 3 – Build and run a job

```python
from foam_agent_mcp_core import build_shell_command, run_foam_agent_process

args, command = build_shell_command(
    config,
    output_dir=Path("./jobs/demo"),
    prompt_path=Path("./prompt.yaml"),
)

print("Executing:", command)
result = run_foam_agent_process(args, cwd=config.root, env={}, timeout=3600)
print(result.stdout[-500:])
```

The helper launches Foam-Agent, captures stdout/stderr, and returns a `CompletedProcess`-like object. You can post-process the logs with your own parser or use the trimming utilities to keep only what agents need.

## Step 4 – Integrate with MCP

```python
from mcp.server.fastmcp import FastMCP
from foam_agent_mcp_core import load_config, build_shell_command, run_foam_agent_process

mcp = FastMCP("foam-agent-mcp", "Foam-Agent automation")
config = load_config()

@mcp.tool()
def run_case(prompt_path: str, output_dir: str = "./jobs/output"):
    args, command = build_shell_command(config, Path(output_dir), Path(prompt_path))
    result = run_foam_agent_process(args, cwd=config.root, env={}, timeout=3600)
    return {"command": command, "stdout": result.stdout, "stderr": result.stderr}

if __name__ == "__main__":
    mcp.run()
```

Now your agent can start CFD jobs with a friendly, auditable interface.

## Tips & extensions

- **Trim archives:** use `foam_agent_mcp_core.trim_archive` to strip large intermediate files before returning results.
- **Async orchestration:** combine this helper with task queues for multi-job scheduling.
- **Teaching moments:** walk students through the generated shell command to demystify Foam-Agent’s CLI flags.

## Development workflow

```bash
uv pip install --system -e .[dev]
uv run ruff check .
uv run pytest
```

Tests stub the Foam-Agent binary so you can examine command construction without running full simulations.

## License

MIT — see [LICENSE](LICENSE).
