"""Runtime helpers for launching Foam-Agent jobs."""

from __future__ import annotations

import shlex
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .config import FoamAgentConfig

MAX_LOG_CHARS = 8000


@dataclass
class ResolveResult:
    value: str | None
    resolved: Path | None


def trim_log(payload: str, limit: int = MAX_LOG_CHARS) -> str:
    """Return the tail of a log to keep responses manageable."""

    if len(payload) <= limit:
        return payload
    return payload[-limit:]


def resolve_path_relative_to_root(config: FoamAgentConfig, candidate: str | None) -> ResolveResult:
    if not candidate:
        return ResolveResult(value=None, resolved=None)

    path = Path(candidate).expanduser()
    if not path.is_absolute():
        path = (config.root / path).resolve()
    return ResolveResult(value=str(path), resolved=path)


def build_shell_command(
    config: FoamAgentConfig,
    output_dir: Path,
    prompt_path: Path,
    custom_mesh_path: str | None,
    extra_args: Iterable[str] | None = None,
) -> tuple[list[str], str]:
    python_cmd = shlex.quote(config.python)
    entrypoint = shlex.quote(str(config.entrypoint))
    openfoam_path = shlex.quote(config.openfoam_path)
    output = shlex.quote(str(output_dir))
    prompt = shlex.quote(str(prompt_path))

    command = [
        f"{python_cmd} {entrypoint}",
        f"--openfoam_path {openfoam_path}",
        f"--output {output}",
        f"--prompt_path {prompt}",
    ]

    if custom_mesh_path:
        command.append(f"--custom_mesh_path {shlex.quote(custom_mesh_path)}")
    if extra_args:
        command.extend(extra_args)

    shell_command = " ".join(command)
    if config.activate:
        shell_command = f"{config.activate} && {shell_command}"

    return ["bash", "-lc", shell_command], shell_command


def run_foam_agent_process(
    args: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    timeout: int | None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
