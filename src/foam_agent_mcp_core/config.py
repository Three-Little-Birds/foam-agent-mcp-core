"""Foam-Agent configuration loading utilities."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FoamAgentConfig:
    root: Path
    entrypoint: Path
    python: str
    activate: str | None
    openfoam_path: str


ENV_ROOT = "FOAM_AGENT_ROOT"
ENV_ENTRYPOINT = "FOAM_AGENT_ENTRYPOINT"
ENV_PYTHON = "FOAM_AGENT_PYTHON"
ENV_ACTIVATE = "FOAM_AGENT_ACTIVATE"
ENV_OPENFOAM_PATH = "FOAM_AGENT_OPENFOAM_PATH"
ENV_OPENFOAM_FALLBACK = "WM_PROJECT_DIR"


def load_config(default_root: Path, env: Mapping[str, str] | None = None) -> FoamAgentConfig:
    """Construct a FoamAgentConfig from environment variables.

    Parameters
    ----------
    default_root:
        Fallback path to the Foam-Agent checkout.
    env:
        Optional mapping providing environment variables (defaults to os.environ).
    """

    env = env or os.environ
    root = Path(env.get(ENV_ROOT, default_root)).expanduser()
    entrypoint_name = env.get(ENV_ENTRYPOINT, "foambench_main.py")
    entrypoint = (root / entrypoint_name).expanduser()
    python_cmd = env.get(ENV_PYTHON, "python")
    activate_cmd = env.get(ENV_ACTIVATE)
    openfoam_path = (
        env.get(ENV_OPENFOAM_PATH) or env.get(ENV_OPENFOAM_FALLBACK) or "/opt/openfoam13"
    )

    return FoamAgentConfig(
        root=root,
        entrypoint=entrypoint,
        python=python_cmd,
        activate=activate_cmd.strip() if activate_cmd else None,
        openfoam_path=str(Path(openfoam_path).expanduser()),
    )
