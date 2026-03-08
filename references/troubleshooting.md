# Troubleshooting

Use this file when webhook setup is broken, the agent cannot reach the portal, or a user asks for help configuring access.

## Default Behavior

Do the first diagnosis yourself before asking the user to copy env vars, confirm internet access, or rerun the same command manually.

Preferred order:

1. inspect saved webhook config
2. inspect current `BITRIX24_WEBHOOK_URL` only as fallback
3. inspect nearby `.env` files if needed
4. validate webhook format
5. resolve DNS for the host
6. probe `user.current.json`
7. report concrete findings and the next fix

Prefer the bundled script:

```bash
python3 <path-to-skill>/scripts/check_webhook.py --json
```

## Typical Failure: curl Exit Code 6

`curl` exit code `6` usually means the host could not be resolved.

Likely causes:

- malformed `BITRIX24_WEBHOOK_URL`
- typo in the portal domain
- env var not loaded in the current shell/session
- stale or missing `.env`
- local DNS or network issue

When you see this:

1. run the webhook check script
2. verify whether the URL came from the environment or an env file
3. keep the webhook itself out of the user-facing reply
4. if DNS fails, say that clearly instead of vaguely saying "JSON formatting problem"

## Typical Failure: Missing Env

If `BITRIX24_WEBHOOK_URL` is missing:

- check saved webhook config first
- check `.env`
- check `.env.local`
- check the current workspace root
- only ask the user for the webhook if no local source exists

Do not ask the user to retype the webhook until you have checked those places.

If the user already pasted the webhook earlier in the conversation, save it immediately and retry from saved config.

## Typical Failure: Bad Format

Expected format:

```text
https://your-portal.bitrix24.ru/rest/<user_id>/<webhook>/
```

Common mistakes:

- missing trailing slash
- copied portal URL instead of webhook URL
- extra quotes or spaces
- wrong user ID segment

## Typical Failure: HTTP 401 or Auth Errors

Usually indicates:

- revoked webhook
- wrong secret
- expired OAuth token
- invalid app auth context

Next actions:

- probe `user.current.json`
- if OAuth is used, verify token freshness and scope
- if webhook is used, ask the user to regenerate or verify the webhook in Bitrix24

## Typical Failure: `ACCESS_DENIED` or `insufficient_scope`

Usually indicates missing permissions.

Tell the user exactly which scope family is likely missing:

- CRM
- Tasks
- Calendar
- Disk
- IM
- `imbot`

Do not just say "permissions issue" without naming the likely scope.

## User-Facing Style

Prefer:

- what you checked
- what failed
- what is already confirmed working
- one next action
- plain business language like "connection to Bitrix24" or "access to calendar"
- doing the next safe diagnostic step yourself before asking the user anything

Avoid:

- long generic lists of shell commands for the user
- asking for confirmation before a simple retry you can do yourself
- exposing the webhook URL, full secret, or masked secret
- talking about `curl`, `MCP`, JSON quoting, `.env`, DNS, or webhook mechanics unless the user explicitly wants technical details
- multiple-choice menus like "1. retry 2. use MCP 3. run it yourself"

## Response Templates

Use short, concrete wording.

Bad:

- "What you need to do now: 1. create env 2. source env 3. run curl 4. or try direct URL 5. or use MCP..."

Better for missing env:

- "Сейчас доступ к Битрикс24 не подключен. Могу сам быстро настроить подключение и сразу проверить связь."

Better when webhook is known from prior context:

- "Подключение к Битрикс24 в этой сессии ещё не сохранено, но я могу сам настроить его и сразу проверить связь."

Better when DNS failed:

- "Сейчас не удаётся связаться с Битрикс24. Похоже, проблема в самом подключении. Следующий шаг: я могу быстро перепроверить доступ и сказать точную причину."

Better when auth failed:

- "Связь с Битрикс24 есть, но доступ не подтверждён. Скорее всего, подключение нужно обновить. Следующий шаг: я могу переподключить доступ и повторить проверку."

Better for non-technical users asking about business tasks:

- "Сейчас не могу получить данные из Битрикс24. Могу сам переподключить доступ и сразу повторить."
- "Сейчас календарь Битрикс24 недоступен. Могу быстро проверить подключение и затем показать расписание."
- "Не удалось связаться с Битрикс24. Могу сам проверить подключение и вернуться с результатом."

## Autonomous Retry Rule

For safe read-only requests:

- run the actual request immediately
- if it fails, run one self-check immediately
- if that can fix the issue, retry once automatically
- only then report the blocker

Examples of safe read-only requests:

- show schedule
- show tasks
- show deals
- check connection
- get current user

Do not ask:

- "Should I try again?"
- "Choose option 1 or 2"
- "Do you want me to run the test now?"

Instead do the test now and return either:

- the actual business result
- or a short blocker in plain language
