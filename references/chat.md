# Chat and Notifications

Use this file for messenger dialogs, chats, history, notifications, and file delivery into chats.

## Separate `im.*` From `imbot.*`

Use `im.*` for normal IM REST methods (webhook-compatible):

- `im.message.add` — send message
- `im.message.update` / `im.message.delete`
- `im.chat.add` / `im.chat.get` / `im.chat.update`
- `im.chat.user.add` / `im.chat.user.delete` / `im.chat.user.list`
- `im.dialog.get` / `im.dialog.messages.get`
- `im.recent.list` / `im.recent.get`
- `im.dialog.writing` — typing indicator

Use `imbot.*` for bot scenarios (requires `CLIENT_ID`):

- `imbot.message.add` / `imbot.message.update` / `imbot.message.delete`
- `imbot.chat.add` / `imbot.dialog.get`
- `imbot.chat.sendTyping`

Do not mix `im.*` and `imbot.*` — pick the family that matches the integration.

## Notifications

- `im.notify.system.add` — system notification (app context only)
- `im.notify.personal.add` — personal notification (app context only)
- `im.notify.read` — mark notification as read

Important: `im.notify.system.add` and `im.notify.personal.add` work only through an application, not plain webhooks. If you get auth errors, this is likely the reason.

## Dialog Addressing

- `123` — direct dialog with user 123
- `chat456` — group chat 456
- `sg789` — group or project chat

## Common Use Cases

### Send a message to a chat

```bash
python3 scripts/bitrix24_call.py im.message.add \
  --param 'DIALOG_ID=chat42' \
  --param 'MESSAGE=Hello team' \
  --json
```

### Read dialog history

```bash
python3 scripts/bitrix24_call.py im.dialog.messages.get \
  --param 'DIALOG_ID=chat42' \
  --param 'LIMIT=20' \
  --json
```

### Send a Disk file to chat

```bash
python3 scripts/bitrix24_call.py im.disk.file.commit \
  --param 'CHAT_ID=42' \
  --param 'FILE_ID[]=5249' \
  --param 'MESSAGE=Project files' \
  --json
```

### Create a group chat

```bash
python3 scripts/bitrix24_call.py im.chat.add \
  --param 'TYPE=CHAT' \
  --param 'TITLE=Project discussion' \
  --param 'USERS[]=1' \
  --param 'USERS[]=2' \
  --json
```

## `CLIENT_ID` for Bots

For `imbot.*` methods:

- Provide `CLIENT_ID` when registering the bot
- Persist it and reuse in every `imbot.*` call
- Treat `CLIENT_ID` as a secret

## Formatting

Bitrix24 chat uses BB-code. Do not double-convert if Markdown is already converted to BB-code.

## Good MCP Queries

- `im message add chat`
- `imbot message`
- `im dialog messages get`
- `im disk file commit`
