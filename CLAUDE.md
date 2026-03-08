# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Bitrix24 skill for OpenClaw — an agent that connects to Bitrix24 via webhook and lets non-technical users (company directors) manage CRM, tasks, calendar, etc. through natural language. Published to ClawHub as `bitrix24`.

## Architecture

Two-layer design:

1. **Python scripts** (`scripts/`) — make REST calls, manage webhook config, diagnose connectivity. No external dependencies beyond Python stdlib (`urllib`, `json`, `ssl`, `socket`).
2. **MCP documentation server** (`https://mcp-dev.bitrix24.tech/mcp`) — provides live method/event/article lookups via `bitrix-search`, `bitrix-method-details`, etc.

All REST calls go through a single webhook URL stored in `~/.config/bitrix24-skill/config.json`.

## Key Files

- `SKILL.md` — **the most important file**. Agent entrypoint: frontmatter (metadata, tags, MCP config), user interaction rules, technical rules, domain reference index. This is what the bot reads to know how to behave.
- `scripts/bitrix24_call.py` — REST caller. Usage: `python3 scripts/bitrix24_call.py <method> --param 'key=value' --json`
- `scripts/bitrix24_config.py` — shared config module: `load_url()`, `validate_url()`, `persist_url_to_config()`
- `scripts/save_webhook.py` — save webhook to config with optional `--check` verification
- `scripts/check_webhook.py` — diagnostics: format → DNS → HTTP probe of `user.current.json`
- `references/*.md` — 16 domain reference files with exact method names, parameters, filter syntax, examples
- `agents/openai.yaml` — OpenAI/OpenClaw agent metadata

## Common Commands

```bash
# Make a REST call
python3 scripts/bitrix24_call.py user.current --json
python3 scripts/bitrix24_call.py crm.deal.list --param 'select[]=ID' --param 'select[]=TITLE' --json

# Save webhook (first-time setup)
python3 scripts/bitrix24_call.py user.current --url "https://portal.bitrix24.ru/rest/1/secret/" --json

# Diagnose webhook
python3 scripts/check_webhook.py --json

# Publish to ClawHub (check current version first)
npx clawhub inspect bitrix24 --versions
npx clawhub publish . --version X.Y.Z

# Install on remote
ssh slon-mac "export PATH=/opt/homebrew/bin:\$PATH; clawhub install bitrix24 --version X.Y.Z --force"
```

## Publishing Workflow

1. Commit and push to `origin/main` (`https://github.com/rsvbitrix/bitrix24-skill.git`)
2. `npx clawhub publish . --version X.Y.Z` — publishes to ClawHub, triggers security scan (~1-2 min)
3. Wait for scan to pass before installing (check with `npx clawhub inspect bitrix24`)
4. On target machine: `clawhub install bitrix24 --version X.Y.Z --force`
5. Restart OpenClaw gateway if agent is cached: `openclaw gateway restart`

## Critical Design Decisions

- **No env vars** — webhook lives only in config JSON, no `.env` files, no `BITRIX24_WEBHOOK_URL`
- **SKILL.md rules go first** — user interaction rules are at the top before any technical content, because the bot must see them before anything else
- **Reference files use `bitrix24_call.py` examples** — not curl, not BX24.js. All examples are copy-paste ready for the agent.
- **Filter operators are key prefixes** — `>=DEADLINE`, `!STATUS`, `>OPPORTUNITY`. This is a common bot mistake; it's documented in SKILL.md rules and reference files.
- **No `calendar.get`** — it doesn't exist. The correct method is `calendar.event.get` with mandatory `type` and `ownerId`. This was a real bot failure that triggered a full MCP audit.

## Bitrix24 API Patterns

- Method names: `module.entity.action` (e.g., `crm.deal.list`, `tasks.task.add`)
- Entity type IDs: 1=lead, 2=deal, 3=contact, 4=company, 7=quote, 31=smart invoice, 128+=custom
- Universal API: `crm.item.*` works across all entity types with `entityTypeId` param
- Fields: UPPER_CASE in classic methods (`crm.deal.*`), camelCase in universal (`crm.item.*`)
- Pagination: page size 50, use `start` parameter
- Dates: ISO 8601 for datetime, `YYYY-MM-DD` for date-only
