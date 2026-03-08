---
name: bitrix24
description: Work with Bitrix24 (Битрикс24) via REST API and the official Bitrix24 MCP documentation server. Use when OpenClaw or Codex needs to manage CRM deals, contacts, leads, companies, tasks, checklists, comments, calendar events, drive files and folders, chats, notifications, users, departments, webhook setup, OAuth setup, or when it must find the exact Bitrix24 method, event, or article before making a call.
metadata:
  openclaw:
    requires:
      bins:
        - python3
      mcp:
        - url: https://mcp-dev.bitrix24.tech/mcp
          transport: streamable_http
          tools:
            - bitrix-search
            - bitrix-app-development-doc-details
            - bitrix-method-details
            - bitrix-article-details
            - bitrix-event-details
    emoji: "B24"
    homepage: https://github.com/rsvbitrix/bitrix24-skill
    aliases:
      - Bitrix24
      - bitrix24
      - Bitrix
      - bitrix
      - b24
      - Битрикс24
      - битрикс24
      - Битрикс
      - битрикс
    tags:
      - bitrix24
      - bitrix
      - b24
      - crm
      - tasks
      - calendar
      - drive
      - chat
      - messenger
      - im
      - webhook
      - oauth
      - mcp
      - Битрикс24
      - CRM
      - задачи
      - чат
---

# Bitrix24

Work with Bitrix24 through two channels:

- **REST calls** through a saved webhook in `~/.config/bitrix24-skill/config.json`
- **Live documentation** through the Bitrix24 MCP server at `https://mcp-dev.bitrix24.tech/mcp`

## Setup

The only thing needed is a webhook URL. When the user provides one, save it and verify:

```bash
python3 scripts/bitrix24_call.py user.current --url "<webhook>" --json
```

This saves the webhook to config and calls `user.current` to verify it works. After that, all calls use the saved config automatically.

If the webhook is not configured yet and you need to set it up, read `references/access.md`.

## Making REST Calls

```bash
python3 scripts/bitrix24_call.py <method> --json
```

Examples:

```bash
python3 scripts/bitrix24_call.py user.current --json
python3 scripts/bitrix24_call.py crm.deal.list \
  --param 'select[]=ID' \
  --param 'select[]=TITLE' \
  --param 'select[]=STAGE_ID' \
  --json
```

If calls fail, read `references/troubleshooting.md` and run `scripts/check_webhook.py --json`.

## Finding the Right Method

When the exact method name is unknown, use MCP docs in this order:

1. `bitrix-search` to find the method, event, or article title.
2. `bitrix-method-details` for REST methods.
3. `bitrix-event-details` for event docs.
4. `bitrix-article-details` for regular documentation articles.
5. `bitrix-app-development-doc-details` for OAuth, install callbacks, BX24 SDK topics.

Do not guess method names from memory when the task is sensitive or the method family is large. Search first.

Then read the domain reference that matches the task:

- `references/crm.md`
- `references/tasks.md`
- `references/chat.md`
- `references/calendar.md`
- `references/drive.md`
- `references/users.md`

## Rules

- Prefer server-side filtering with `filter[...]` and narrow output with `select[]`.
- Use `*.fields` or user-field discovery methods before writing custom fields.
- Expect pagination on list methods via `start` or method-specific `START`.
- Use ISO 8601 date-time strings when a method expects a date-time value.
- Treat `ACCESS_DENIED`, `insufficient_scope`, `QUERY_LIMIT_EXCEEDED`, and `expired_token` as normal operational cases.
- For `imbot.*`, persist and reuse the same `CLIENT_ID`.
- When a call fails, run `scripts/check_webhook.py --json` before asking the user.
- In user-facing replies, talk about "connection to Bitrix24" in plain language. Do not show webhook URLs, secrets, curl, MCP, DNS, or JSON details unless explicitly asked.
- For safe read-only requests ("show my schedule", "list my tasks", "show deals"), execute immediately without asking permission. Do one automatic retry on failure.
- Do not present multiple-choice troubleshooting options. Either do the next safe step yourself or report one concise blocker.
- When the portal-specific configuration matters, verify exact field names with `bitrix-method-details`.

## Domain References

- `references/access.md` — webhook setup, OAuth, install callbacks.
- `references/troubleshooting.md` — diagnostics and self-repair.
- `references/mcp-workflow.md` — MCP tool selection and query patterns.
- `references/crm.md` — deals, contacts, leads, companies, activities.
- `references/tasks.md` — tasks, checklists, comments, planner.
- `references/chat.md` — im, imbot, notifications, dialog history.
- `references/calendar.md` — sections, events, attendees, availability.
- `references/drive.md` — storage, folders, files, external links.
- `references/users.md` — users, departments, org-structure.

Read only the reference file that matches the current task.
