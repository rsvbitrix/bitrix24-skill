---
name: bitrix24
description: Work with Bitrix24 (Битрикс24) via REST API and the official Bitrix24 MCP documentation server. Use when OpenClaw or Codex needs to manage CRM deals, contacts, leads, companies, smart processes, quotes, invoices, products, tasks, checklists, comments, calendar events, drive files and folders, chats, notifications, users, departments, org structure, projects and workgroups, activity feed, time tracking, work reports, landing pages, sites, webhook setup, OAuth setup, or when it must find the exact Bitrix24 method, event, or article before making a call.
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
      - проекты
      - группы
      - лента
      - рабочее время
      - timeman
      - socialnetwork
      - feed
      - projects
      - workgroups
      - org structure
      - smart process
      - смарт-процесс
      - products
      - товары
      - каталог
      - quotes
      - предложения
      - invoices
      - счета
      - landing
      - sites
      - сайты
      - лендинги
---

# Bitrix24

## STOP — Read These Rules Before Doing Anything

You are talking to a business person (company director), NOT a developer. They do not know what an API is. They do not want to see technical details. Every violation of these rules makes the user angry.

### Rule 1: Read requests — EXECUTE IMMEDIATELY

When the user asks to see, show, list, or check anything — DO IT RIGHT NOW. Do not ask questions. Do not ask for confirmation. Do not offer choices. Just call the Bitrix24 methods and show the result.

User says "дай расписание на среду" → you IMMEDIATELY:
1. Call `user.current` to get user ID and timezone
2. Call `calendar.event.get` for that date (read `references/calendar.md` for exact syntax)
3. Call `tasks.task.list` with deadline filter for that date (read `references/tasks.md`)
4. Show combined schedule in a clean list

User says "покажи сделки" → you IMMEDIATELY call `crm.deal.list` and show results.

User says "мои задачи" → you IMMEDIATELY call `tasks.task.list` and show results.

### Rule 2: NEVER show technical details

These words are FORBIDDEN in your replies to the user:
API, REST, webhook, MCP, endpoint, scope, token, curl, JSON, method, parameter, SDK, OAuth, calendar.event.get, tasks.task.list, crm.deal.list, bitrix24_call.py, config.json

WRONG replies (NEVER do this):
- "Используем ваш webhook URL bitrix24.team/rest/5/..." — FORBIDDEN
- "Вызовем calendar.get или calendar.event.get..." — FORBIDDEN
- "Пришлите экспорт календаря (ICS/CSV)..." — FORBIDDEN
- "Подтвердите часовой пояс..." — FORBIDDEN
- "Подтвердите источник данных..." — FORBIDDEN
- "Как предпочитаете продолжить?" — FORBIDDEN for read requests

CORRECT replies:
- "Вот ваше расписание на среду, 11 марта:" followed by the data
- "Открытые сделки:" followed by the list
- "Ваши задачи на сегодня:" followed by the list

### Rule 3: Write requests — one short yes/no question

For creating, updating, or deleting: confirm in one sentence.
- CORRECT: "Создать сделку «Поставка» на 500 000 ₽?"
- WRONG: "Вызовем crm.deal.add с параметрами..."

### Rule 4: Errors — fix silently or say one sentence

If a call fails, retry automatically. If still fails: "Не удалось подключиться к Битрикс24, проверьте, что портал доступен." Nothing else.

### Rule 5: Language and format

- Reply in the same language the user writes in
- Present data as clean tables or bullet lists
- Use business words: "сделка", "задача", "контакт", "встреча", "расписание"
- For schedule requests: combine calendar events AND task deadlines into one view
- Get timezone from `user.current`, never ask the user

---

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
- `references/smartprocess.md`
- `references/products.md`
- `references/quotes.md`
- `references/tasks.md`
- `references/chat.md`
- `references/calendar.md`
- `references/drive.md`
- `references/users.md`
- `references/projects.md`
- `references/feed.md`
- `references/timeman.md`
- `references/sites.md`

## Technical Rules

These rules are for the agent internally, not for user-facing output.

- Start with `user.current` to get the webhook user's ID — many methods need `ownerId` or `RESPONSIBLE_ID`.
- Do not invent method names. There is no `calendar.get`, `tasks.list`, etc. Always use exact names from the reference files or MCP search. When unsure, search MCP first.
- Prefer server-side filtering with `filter[...]` and narrow output with `select[]`.
- Filter operators are prefixes on the key: `>=DEADLINE`, `!STATUS`, `>OPPORTUNITY`. Not on the value.
- Use `*.fields` or user-field discovery methods before writing custom fields.
- Expect pagination on list methods via `start` (page size = 50).
- Use ISO 8601 date-time strings for datetime fields, `YYYY-MM-DD` for date-only fields.
- Treat `ACCESS_DENIED`, `insufficient_scope`, `QUERY_LIMIT_EXCEEDED`, and `expired_token` as normal operational cases.
- For `imbot.*`, persist and reuse the same `CLIENT_ID`.
- When a call fails, run `scripts/check_webhook.py --json` before asking the user.
- When the portal-specific configuration matters, verify exact field names with `bitrix-method-details`.

## Domain References

- `references/access.md` — webhook setup, OAuth, install callbacks.
- `references/troubleshooting.md` — diagnostics and self-repair.
- `references/mcp-workflow.md` — MCP tool selection and query patterns.
- `references/crm.md` — deals, contacts, leads, companies, activities.
- `references/smartprocess.md` — smart processes, funnels, stages, universal crm.item API.
- `references/products.md` — product catalog, product rows on deals/quotes/invoices.
- `references/quotes.md` — quotes (commercial proposals), smart invoices.
- `references/tasks.md` — tasks, checklists, comments, planner.
- `references/chat.md` — im, imbot, notifications, dialog history.
- `references/calendar.md` — sections, events, attendees, availability.
- `references/drive.md` — storage, folders, files, external links.
- `references/users.md` — users, departments, org-structure, subordinates.
- `references/projects.md` — workgroups, projects, scrum, membership.
- `references/feed.md` — activity stream, feed posts, comments.
- `references/timeman.md` — time tracking, work day, absence reports, task time.
- `references/sites.md` — landing pages, sites, blocks, publishing.

Read only the reference file that matches the current task.

Note: Bitrix24 has no REST API for reading or sending emails. `mailservice.*` only configures SMTP/IMAP services.
