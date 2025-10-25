from __future__ import annotations

import os
from pathlib import Path

import pytest

from foam_agent_mcp_core import (
    FoamAgentConfig,
    build_shell_command,
    load_config,
    resolve_path_relative_to_root,
)


@pytest.fixture
def config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> FoamAgentConfig:
    root = tmp_path / "foam-agent"
    root.mkdir()
    entrypoint = root / "foambench_main.py"
    entrypoint.write_text("print('stub')\n", encoding="utf-8")

    monkeypatch.setenv("FOAM_AGENT_ROOT", str(root))
    monkeypatch.setenv("FOAM_AGENT_ENTRYPOINT", "foambench_main.py")
    monkeypatch.setenv("FOAM_AGENT_PYTHON", "python")
    monkeypatch.delenv("FOAM_AGENT_ACTIVATE", raising=False)

    return load_config(default_root=root)


def test_resolve_custom_mesh_relative_path(config: FoamAgentConfig) -> None:
    mesh = config.root / "meshes" / "mesh.stl"
    mesh.parent.mkdir(parents=True, exist_ok=True)
    mesh.write_text("stub", encoding="utf-8")

    result = resolve_path_relative_to_root(config, "meshes/mesh.stl")

    assert result.value is not None
    assert result.resolved is not None
    assert result.resolved.exists()


def test_build_shell_command_contains_prompt_and_output(config: FoamAgentConfig, tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    prompt_path = tmp_path / "prompt.txt"
    prompt_path.write_text("hello", encoding="utf-8")

    args, shell_command = build_shell_command(
        config,
        output_dir=output_dir,
        prompt_path=prompt_path,
        custom_mesh_path=None,
    )

    assert args[0:2] == ["bash", "-lc"]
    assert str(output_dir) in shell_command
    assert str(prompt_path) in shell_command
    assert "--custom_mesh_path" not in shell_command
