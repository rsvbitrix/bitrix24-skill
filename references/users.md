# Users and Structure

Use this file for user lookup, department structure, messenger-side org search, and colleague resolution.

## Core Methods

Users:

- `user.current` — current webhook user (use to get own ID)
- `user.get` — get users by filter
- `user.search` — fast fuzzy search by name, position, department
- `profile` — basic info about current user (no scope required)

Departments:

- `department.get` — list departments
- `department.add` / `department.update` / `department.delete`
- `department.fields` — field schema

Messenger-side helpers:

- `im.department.employees.get` — employees of a department
- `im.department.colleagues.list` — current user's colleagues
- `im.search.user.list` — search users by name/position
- `im.search.department.list` — search departments by name
- `im.user.get` — get user data by ID

`BX24.selectUsers` is a frontend-only helper, not usable from REST.

## Common Use Cases

### Get current user identity

Always start with this to know the webhook user ID:

```bash
python3 scripts/bitrix24_call.py user.current --json
```

### Search users by name

```bash
python3 scripts/bitrix24_call.py user.search \
  --param 'FILTER[NAME]=Ivan' \
  --json
```

### Get users by department

```bash
python3 scripts/bitrix24_call.py user.get \
  --param 'filter[UF_DEPARTMENT]=5' \
  --json
```

### List all departments

```bash
python3 scripts/bitrix24_call.py department.get --json
```

### Get employees of a department (via messenger API)

```bash
python3 scripts/bitrix24_call.py im.department.employees.get \
  --param 'ID[]=5' \
  --json
```

## Working Rules

- Use `user.current` first to get own user ID — needed for calendar, tasks, and other methods.
- Use `user.search` for fast fuzzy lookups.
- Use `department.get` for org structure.
- Use `im.department.*` for messenger-oriented lookups.

## Good MCP Queries

- `user current get search`
- `department get fields`
- `im department employees colleagues`
- `im search user`
