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
5. [Accessibility & upkeep](#accessibility--upkeep)
6. [Contributing](#contributing)

## What it provides

| Scenario | Value |
|----------|-------|
| Foam-Agent job control | Start [Foam-Agent](https://github.com/csml-rpi/Foam-Agent) cases, watch logs, and collect archives without rewriting boilerplate. |
| OpenFOAM/conda setup | Discover OpenFOAM paths, conda environments, and activation scripts so services can bootstrap consistently. |
| Metrics archival | Emit JSON metrics compatible with the Continuous Evidence Engine for downstream reporting. |

## Quickstart

```bash
uv pip install "git+https://github.com/Three-Little-Birds/foam-agent-mcp-core.git"
```

See `examples/` for a minimal job submission that writes archives to `logs/foam_agent/`.

## Key modules

- `foam_agent_mcp_core.config` - locate Foam-Agent entry points, activate conda envs.
- `foam_agent_mcp_core.runner` - submit jobs, stream logs, and capture exit codes.
- `foam_agent_mcp_core.metrics` - write JSON metrics (lift, drag, stiffness, etc.) for the Continuous Evidence Engine.

## Stretch ideas

1. Add GPU-aware runners to pair with future CUDA containers.
2. Extend metrics to include Reynolds/Strouhal calculations for dashboards.
3. Ship templated prompts for common case types (gust rejection, stiffness sweeps).

## Accessibility & upkeep

- Configure Foam-Agent/OpenFOAM paths via `foam_agent_mcp_core.config` so services run without hard-coded directories.
- Document any additional metrics or archive conventions in PRs to keep downstream services consistent.

## Contributing

1. `uv pip install --system -e .[dev]`
2. Run `uv run ruff check .` and `uv run pytest`
3. Document new helpers and prompt templates in the README to keep service authors in sync.

MIT license - see [LICENSE](LICENSE).
