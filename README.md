# foam-agent-mcp-core - OpenFOAM automation primitives for MCP services

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB.svg" alt="Python 3.10 or newer"></a>
  <img src="https://img.shields.io/badge/MCP-core-blueviolet.svg" alt="MCP core badge">
</p>

> **TL;DR**: Shared helpers for launching Foam-Agent/OpenFOAM jobs, archiving results, and emitting MCP-friendly metadata.

## Table of contents

1. [What it provides](#what-it-provides)
2. [Quickstart](#quickstart)
3. [Key modules](#key-modules)
4. [Stretch ideas](#stretch-ideas)
5. [Install & maintenance](#install--maintenance)
6. [Contributing](#contributing)

## What it provides

| Scenario | Value |
|----------|-------|
| Foam-Agent job control | Start [Foam-Agent](https://github.com/csml-rpi/Foam-Agent) cases, watch logs, and collect archives without rewriting boilerplate. |
| OpenFOAM/conda setup | Discover OpenFOAM paths, conda environments, and activation scripts so services can bootstrap consistently. |
| Metrics archival | Emit JSON metrics that downstream dashboards and reports can ingest. |

## Quickstart

```bash
uv pip install "git+https://github.com/Three-Little-Birds/foam-agent-mcp-core.git"
```

Minimal job submission (writes to `logs/foam_agent/`):

```python
from pathlib import Path
import os

from foam_agent_mcp_core.config import load_config
from foam_agent_mcp_core.runtime import build_shell_command, run_foam_agent_process

# Point to your Foam-Agent checkout; environment variables override these defaults.
config = load_config(Path("~/foam-agent"))

output_dir = Path("logs/foam_agent/manual-run")
output_dir.mkdir(parents=True, exist_ok=True)
prompt_path = config.root / "prompts" / "gust_rejection.json"

args, preview = build_shell_command(
    config,
    output_dir=output_dir,
    prompt_path=prompt_path,
    custom_mesh_path=None,
    extra_args=["--job_label", "demo-run"],
)
print("Launching:", preview)
result = run_foam_agent_process(
    args,
    cwd=config.root,
    env=os.environ.copy(),
    timeout=3600,
)
result.check_returncode()
print("Job archive:", output_dir)
```

## Key modules

- `foam_agent_mcp_core.config` - locate Foam-Agent entry points, activate conda envs.
- `foam_agent_mcp_core.runner` - submit jobs, stream logs, and capture exit codes.
- `foam_agent_mcp_core.metrics` - write JSON metrics (lift, drag, stiffness, etc.) for downstream scorecards.

## Stretch ideas

1. Add GPU-aware runners to pair with future CUDA containers.
2. Extend metrics to include Reynolds/Strouhal calculations for dashboards.
3. Ship templated prompts for common case types (gust rejection, stiffness sweeps).

## Install & maintenance

- **Runtime install:** follow the [Quickstart](#quickstart) `uv pip install "git+https://github.com/Three-Little-Birds/foam-agent-mcp-core.git"` step on any host that needs the helpers.
- **Environment configuration:** use `foam_agent_mcp_core.config.find_install()` to point at OpenFOAM/conda locations instead of hard-coding paths in services.
- **Archive & metrics conventions:** document any additional JSON metrics or archive naming schemes in PRs so dependent MCPs stay compatible.

## Contributing

1. `uv pip install --system -e .[dev]`
2. Run `uv run ruff check .` and `uv run pytest`
3. Document new helpers and prompt templates in the README to keep service authors in sync.

MIT license - see [LICENSE](LICENSE).
