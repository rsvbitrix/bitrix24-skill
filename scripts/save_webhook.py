#!/usr/bin/env python3
"""Save a Bitrix24 webhook into stable config and optionally env files."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from bitrix24_config import DEFAULT_CONFIG_PATH, load_config, save_config, validate_url  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save a Bitrix24 webhook into stable config.")
    parser.add_argument("--url", required=True, help="Bitrix24 webhook URL")
    parser.add_argument("--config-file", default=str(DEFAULT_CONFIG_PATH), help="Target config file path")
    parser.add_argument(
        "--env-file",
        action="append",
        default=[],
        help="Optional env file to update for compatibility (repeatable)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing saved webhook")
    parser.add_argument("--check", action="store_true", help="Run check_webhook.py after saving")
    return parser.parse_args()


def load_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8").splitlines()


def save_env(path: Path, url: str, force: bool) -> tuple[bool, bool]:
    lines = load_lines(path)
    new_line = f'BITRIX24_WEBHOOK_URL="{url}"'
    found = False
    changed = False
    out: list[str] = []

    for raw in lines:
        stripped = raw.strip()
        candidate = stripped[7:].strip() if stripped.startswith("export ") else stripped
        if candidate.startswith("BITRIX24_WEBHOOK_URL="):
            found = True
            if force:
                out.append(new_line)
                changed = raw != new_line
            else:
                out.append(raw)
            continue
        out.append(raw)

    if not found:
        if out and out[-1] != "":
            out.append("")
        out.append(new_line)
        changed = True

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return found, changed


def run_check(config_path: Path, env_files: list[str]) -> int:
    script = Path(__file__).with_name("check_webhook.py")
    cmd = [sys.executable, str(script), "--config-file", str(config_path), "--json"]
    for env_file in env_files:
        cmd.extend(["--env-file", env_file])
    result = subprocess.run(cmd, check=False)
    return result.returncode


def main() -> int:
    args = parse_args()
    try:
        normalized = validate_url(args.url)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    config_path = Path(args.config_file).expanduser()
    config = load_config(config_path)
    found = isinstance(config.get("webhook_url"), str) and bool(config.get("webhook_url"))
    if found and not args.force:
        changed = False
    else:
        config["webhook_url"] = normalized
        save_config(config_path, config)
        changed = True

    for env_file_raw in args.env_file:
        save_env(Path(env_file_raw).expanduser(), normalized, args.force)

    print(f"saved_to: {config_path}")
    if found and not args.force:
        print("note: saved webhook already existed and was kept unchanged; use --force to replace it")
    elif found and args.force:
        print("note: existing saved webhook was replaced")
    elif changed:
        print("note: webhook was saved")

    if args.env_file:
        print("note: compatibility env files were updated too")

    if args.check:
        return run_check(config_path, args.env_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
