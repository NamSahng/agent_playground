#!/usr/bin/env python3
"""Example-local adapter; leave the pinned upstream skill and user config intact."""
import importlib.util
import json
import os
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "upstream_runner", ROOT / ".agents/skills/claudex-loop/scripts/runner.py")
upstream = importlib.util.module_from_spec(spec)
spec.loader.exec_module(upstream)
original_command = upstream.command
original_git = upstream.git


def scoped_git(repo, *args):
    # Upstream assumes repo is the Git root. This playground is a subtree.
    # Keep both the diff and untracked manifest relative to that subtree, and
    # retain outputs in Git without feeding old model transcripts into reviews.
    args = list(args)
    if args[0] == "diff":
        args.insert(1, "--relative")
        if "--" in args:
            args = args[:args.index("--")]
        args += ["--", ".", ":(exclude)output/**"]
    elif args[0] == "ls-files":
        args += ["--", ".", ":(exclude)output/**"]
    return original_git(repo, *args)


def codex_overrides():
    # Read only configuration metadata, never print auth or configuration values.
    personal = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "config.toml"
    paths = [Path("/etc/codex/config.toml"), personal]
    paths += [p / ".codex/config.toml" for p in reversed((ROOT, *ROOT.parents))]
    servers = set()
    defaults = {}
    for path in paths:
        if path.is_file():
            config = tomllib.loads(path.read_text())
            servers.update(config.get("mcp_servers", {}))
            if path == personal:
                defaults = {key: config[key] for key in ("model", "model_reasoning_effort") if key in config}
    flags = ["--ignore-user-config"]
    for feature in ("plugins", "apps", "hooks", "skill_mcp_dependency_install"):
        flags += ["-c", f"features.{feature}=false"]
    for server in sorted(servers):
        flags += ["-c", f"mcp_servers.{json.dumps(server)}.enabled=false"]
    for key, value in defaults.items():
        flags += ["-c", f"{key}={json.dumps(value)}"]
    return flags


def command(provider, mode, run_dir, model=None, effort=None, session=None):
    args = original_command(provider, mode, run_dir, model, effort, session)
    if provider == "codex":
        # Defaults first: explicit per-call model/effort remain authoritative.
        args[1:1] = codex_overrides()
    return args


upstream.command = command
upstream.git = scoped_git

if __name__ == "__main__":
    raise SystemExit(upstream.main())
