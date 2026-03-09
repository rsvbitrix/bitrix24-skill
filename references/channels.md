# Channels (Каналы)

Use this file for Bitrix24 channels — broadcast-style chats where only owners/managers post and subscribers read.

Channels are a special chat type (`type: openChannel`, `ENTITY_TYPE: ANNOUNCEMENT`).
They use standard `im.*` methods — there is no separate `im.channel.*` API.

## How Channels Differ From Chats

| Feature | Chat | Channel |
|---------|------|---------|
| Who can post | All members | Only owner + managers |
| `type` in API | `chat` / `open` | `openChannel` |
| Create with | `TYPE=CHAT` or `TYPE=OPEN` | `ENTITY_TYPE=ANNOUNCEMENT` |
| List only these | `SKIP_CHAT=N` | `ONLY_CHANNEL=Y` |
| Join | By invite | Self-subscribe (open) or invite |

## Core Methods

All use the same `im.*` family:

Create & manage:

- `im.chat.add` — create channel (with `ENTITY_TYPE=ANNOUNCEMENT`)
- `im.chat.updateTitle` — rename channel
- `im.chat.setOwner` — transfer ownership
- `im.chat.mute` — mute/unmute notifications

List & find:

- `im.recent.list` — list channels (`ONLY_CHANNEL=Y`)
- `im.dialog.get` — get channel info (returns `type: openChannel`)
- `im.search.chat.list` — search channels by name
- `im.counters.get` — unread counters (includes channel counters)

Messages:

- `im.message.add` — post to channel (owner/managers only)
- `im.dialog.messages.get` — read channel history
- `im.dialog.messages.search` — search messages in channel

Subscribers:

- `im.chat.user.add` — add subscribers
- `im.chat.user.delete` — remove subscribers
- `im.chat.user.list` — list subscribers
- `im.chat.leave` — unsubscribe (current user leaves)

Pin & hide:

- `im.recent.pin` — pin channel at top of list
- `im.recent.hide` — hide channel from recent list

## Common Use Cases

### Create a channel

```bash
python3 scripts/bitrix24_call.py im.chat.add \
  --param 'TYPE=OPEN' \
  --param 'ENTITY_TYPE=ANNOUNCEMENT' \
  --param 'TITLE=Company News' \
  --param 'DESCRIPTION=Official company announcements' \
  --param 'USERS[]=1' \
  --param 'USERS[]=2' \
  --param 'MESSAGE=Welcome to the channel!' \
  --json
```

Returns channel chat ID. Creator becomes the owner.

### List all channels

```bash
python3 scripts/bitrix24_call.py im.recent.list \
  --param 'ONLY_CHANNEL=Y' \
  --param 'LIMIT=50' \
  --json
```

Filter channels with `ONLY_CHANNEL=Y`. Each result contains `type: openChannel`.

### Post to a channel

```bash
python3 scripts/bitrix24_call.py im.message.add \
  --param 'DIALOG_ID=chat42' \
  --param 'MESSAGE=Important update: new office hours starting Monday' \
  --json
```

Only the channel owner and managers can post. Regular subscribers get `ACCESS_ERROR`.

### Read channel messages

```bash
python3 scripts/bitrix24_call.py im.dialog.messages.get \
  --param 'DIALOG_ID=chat42' \
  --param 'LIMIT=20' \
  --json
```

### Get channel info

```bash
python3 scripts/bitrix24_call.py im.dialog.get \
  --param 'DIALOG_ID=chat42' \
  --json
```

Returns object with `type: openChannel`, owner, name, description, subscriber count.

### Search for a channel by name

```bash
python3 scripts/bitrix24_call.py im.search.chat.list \
  --param 'FIND=News' \
  --param 'LIMIT=10' \
  --json
```

Returns all matching chats. Filter by `type: openChannel` in results to get channels only.

### Add subscribers to channel

```bash
python3 scripts/bitrix24_call.py im.chat.user.add \
  --param 'CHAT_ID=42' \
  --param 'USERS[]=5' \
  --param 'USERS[]=6' \
  --param 'USERS[]=7' \
  --json
```

### List channel subscribers

```bash
python3 scripts/bitrix24_call.py im.chat.user.list \
  --param 'CHAT_ID=42' \
  --json
```

### Unsubscribe from channel

```bash
python3 scripts/bitrix24_call.py im.chat.leave \
  --param 'CHAT_ID=42' \
  --json
```

### Rename a channel

```bash
python3 scripts/bitrix24_call.py im.chat.updateTitle \
  --param 'CHAT_ID=42' \
  --param 'TITLE=Company Updates 2026' \
  --json
```

### Mute channel notifications

```bash
python3 scripts/bitrix24_call.py im.chat.mute \
  --param 'CHAT_ID=42' \
  --param 'MUTE=Y' \
  --json
```

`MUTE=Y` to mute, `MUTE=N` to unmute.

### Pin channel at top of chat list

```bash
python3 scripts/bitrix24_call.py im.recent.pin \
  --param 'DIALOG_ID=chat42' \
  --param 'PIN=Y' \
  --json
```

## Working Rules

- Channels have NO separate API — use `im.*` methods with `ENTITY_TYPE=ANNOUNCEMENT`.
- Identify channels by `type: openChannel` in responses from `im.dialog.get` or `im.recent.list`.
- Only owner and managers can post (`im.message.add`). Subscribers get `ACCESS_ERROR`.
- To make someone a manager, use `im.chat.setOwner` (transfers ownership) — there is no separate "set manager" method via REST.
- Use `ONLY_CHANNEL=Y` in `im.recent.list` to filter channels from regular chats.
- Channel `DIALOG_ID` format: `chatXXX` (same as regular group chats).
- Subscribers can leave with `im.chat.leave`, but cannot be re-added without owner action.
- `im.search.chat.list` returns both chats and channels — filter results by `type` field.

## Good MCP Queries

- `im chat add`
- `im recent list`
- `im dialog get`
- `im chat user add`
- `im chat mute`
- `im recent pin`
- `im search chat list`
