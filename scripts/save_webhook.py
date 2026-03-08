#!/usr/bin/env python3
"""
Save BITRIX24_WEBHOOK_URL into an env file and optionally verify it.

This script does not mutate the parent shell environment directly.
It persists the webhook to an env file that the skill can reuse.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

WEBHOOK_RE = re.compile(r"^https://(?P<host>[^/]+)/rest/(?P<user_id>\d+)/(?P<secret>[^/]+)/?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save a Bitrix24 webhook into an env file.")
    parser.add_argument("--url", required=True, help="Bitrix24 webhook URL")
    parser.add_argument("--env-file", default=".env", help="Target env file path")
    parser.add_argument("--force", action="store_true", help="Overwrite existing BITRIX24_WEBHOOK_URL")
    parser.add_argument("--check", action="store_true", help="Run check_webhook.py after saving")
    return parser.parse_args()


def normalize_url(value: str) -> str:
    return value.strip().strip('"').strip("'").rstrip("/") + "/"


def mask_url(value: str) -> str:
    match = WEBHOOK_RE.match(value)
    if not match:
        return value
    secret = match.group("secret")
    if len(secret) <= 4:
        masked = "*" * len(secret)
    else:
        masked = f"{secret[:2]}***{secret[-2:]}"
    return f"https://{match.group('host')}/rest/{match.group('user_id')}/{masked}/"


def validate_url(value: str) -> str:
    normalized = normalize_url(value)
    if not WEBHOOK_RE.match(normalized):
        raise ValueError("Webhook format is invalid. Expected https://<host>/rest/<user_id>/<secret>/")
    return normalized


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


def run_check(path: Path) -> int:
    script = Path(__file__).with_name("check_webhook.py")
    result = subprocess.run(
        [sys.executable, str(script), "--env-file", str(path), "--json"],
        check=False,
    )
    return result.returncode


def main() -> int:
    args = parse_args()
    try:
        normalized = validate_url(args.url)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    env_file = Path(args.env_file).expanduser()
    found, changed = save_env(env_file, normalized, args.force)

    print(f"saved_to: {env_file}")
    if found and not args.force:
        print("note: BITRIX24_WEBHOOK_URL already existed and was kept unchanged; use --force to replace it")
    elif found and args.force:
        print("note: existing BITRIX24_WEBHOOK_URL was replaced")
    elif changed:
        print("note: BITRIX24_WEBHOOK_URL was added")

    print("note: the current parent shell env is not changed automatically; the env file was updated for future use")

    if args.check:
        return run_check(env_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
