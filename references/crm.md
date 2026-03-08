# CRM

Use this file for deals, contacts, companies, leads, activities, and modern CRM item APIs.

## Core Methods

Deals:

- `crm.deal.list` / `crm.deal.get` / `crm.deal.add` / `crm.deal.update` / `crm.deal.delete`
- `crm.deal.fields` — field schema
- `crm.deal.contact.add` / `crm.deal.contact.items.get`

Contacts:

- `crm.contact.list` / `crm.contact.get` / `crm.contact.add` / `crm.contact.update` / `crm.contact.delete`
- `crm.contact.fields`

Companies:

- `crm.company.list` / `crm.company.get` / `crm.company.add` / `crm.company.update` / `crm.company.delete`

Leads:

- `crm.lead.list` / `crm.lead.get` / `crm.lead.add` / `crm.lead.update` / `crm.lead.delete`
- `crm.lead.fields`

Activities:

- `crm.activity.list` / `crm.activity.add` / `crm.activity.update` / `crm.activity.delete`

Modern generalized APIs (smart processes, dynamic types):

- `crm.item.list` / `crm.item.add` / `crm.item.update` / `crm.item.delete`
- `crm.item.batchImport`

## Filter Syntax

CRM list methods use prefix operators:

- `>OPPORTUNITY` — greater than
- `>=DATE_CREATE` — on or after
- `=STAGE_ID` — equals (default without prefix)
- `!STATUS_ID` — not equal

Example: `filter[>OPPORTUNITY]=10000` returns deals with opportunity above 10000.

## Common Use Cases

### List deals with filter

```bash
python3 scripts/bitrix24_call.py crm.deal.list \
  --param 'filter[>OPPORTUNITY]=10000' \
  --param 'select[]=ID' \
  --param 'select[]=TITLE' \
  --param 'select[]=OPPORTUNITY' \
  --param 'select[]=STAGE_ID' \
  --json
```

### Create a deal

```bash
python3 scripts/bitrix24_call.py crm.deal.add \
  --param 'fields[TITLE]=New Deal' \
  --param 'fields[OPPORTUNITY]=50000' \
  --param 'fields[CURRENCY_ID]=RUB' \
  --json
```

### Get field schema before writing

```bash
python3 scripts/bitrix24_call.py crm.deal.fields --json
```

### Add activity to a deal

```bash
python3 scripts/bitrix24_call.py crm.activity.add \
  --param 'fields[OWNER_TYPE_ID]=2' \
  --param 'fields[OWNER_ID]=123' \
  --param 'fields[TYPE_ID]=2' \
  --param 'fields[SUBJECT]=Follow-up call' \
  --json
```

### Stuck deals (no activity for 14+ days)

Deals in active pipeline with no recent modification — useful for proactive "💤" warnings:

```bash
python3 scripts/bitrix24_call.py crm.deal.list \
  --param 'filter[ASSIGNED_BY_ID]=1' \
  --param 'filter[STAGE_SEMANTIC_ID]=P' \
  --param 'filter[<DATE_MODIFY]=2026-02-22' \
  --param 'select[]=ID' \
  --param 'select[]=TITLE' \
  --param 'select[]=STAGE_ID' \
  --param 'select[]=DATE_MODIFY' \
  --param 'select[]=OPPORTUNITY' \
  --json
```

`STAGE_SEMANTIC_ID=P` = in progress (active pipeline). `<DATE_MODIFY` = last modified before 14 days ago.

## Working Rules

- Read `*.fields` before writing custom or portal-specific fields.
- Do not hardcode stage names across portals — pipelines and categories vary.
- Use classic `crm.deal.*` for built-in entities, `crm.item.*` for smart processes.
- Always use `select[]` to limit response size.
- Pagination: page size is 50, use `start=0`, `start=50`, etc.

## Good MCP Queries

- `crm deal list add update`
- `crm contact company`
- `crm lead fields`
- `crm activity`
- `crm item smart process`
