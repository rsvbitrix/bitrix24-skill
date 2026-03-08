#!/usr/bin/env python3
"""Shared helpers for Bitrix24 skill scripts."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

WEBHOOK_RE = re.compile(r"^https://(?P<host>[^/]+)/rest/(?P<user_id>\d+)/(?P<secret>[^/]+)/?$")
DEFAULT_CONFIG_PATH = Path.home() / ".config" / "bitrix24-skill" / "config.json"


def normalize_url(value: str) -> str:
    return value.strip().strip('"').strip("'").rstrip("/") + "/"


def validate_url(value: str) -> str:
    normalized = normalize_url(value)
    if not WEBHOOK_RE.match(normalized):
        raise ValueError("Webhook format is invalid. Expected https://<host>/rest/<user_id>/<secret>/")
    return normalized


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


def read_env_file(path: Path) -> str | None:
    if not path.is_file():
        return None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if not line.startswith("BITRIX24_WEBHOOK_URL="):
            continue
        return line.split("=", 1)[1].strip()
    return None


def candidate_env_files(extra: list[str]) -> list[Path]:
    paths: list[Path] = []
    for item in extra:
        path = Path(item).expanduser()
        if path not in paths:
            paths.append(path)

    cwd = Path.cwd()
    for base in [cwd, cwd.parent]:
        for name in [".env", ".env.local", ".env.development", ".env.production"]:
            path = base / name
            if path not in paths:
                paths.append(path)
    return paths


def load_config(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def save_config(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def load_url(
    *,
    cli_url: str | None,
    config_file: str | None = None,
    env_files: list[str] | None = None,
) -> tuple[str | None, str]:
    if cli_url:
        return cli_url, "arg:url"

    env_value = os.environ.get("BITRIX24_WEBHOOK_URL")
    if env_value:
        return env_value, "env:BITRIX24_WEBHOOK_URL"

    config_path = Path(config_file).expanduser() if config_file else DEFAULT_CONFIG_PATH
    config = load_config(config_path)
    config_url = config.get("webhook_url")
    if isinstance(config_url, str) and config_url.strip():
        return config_url, f"config:{config_path}"

    for path in candidate_env_files(env_files or []):
        value = read_env_file(path)
        if value:
            return value, f"env-file:{path}"

    return None, "missing"
