---
name: json-schema-validator
description: "Validate a dict/JSON payload against a useful subset of JSON Schema (type, required, properties, items, enum, min/max, length) with zero dependencies, returning readable errors. Use when the user wants to validate a webhook payload, API response, or config against a schema, or gate bad data before processing - without adding the jsonschema package."
version: "1.0.0"
---

# JSON Schema Validator (zero-dep)

Use this skill to gate untrusted JSON - a webhook body, an API response, a config file - before your pipeline acts on it, without pulling in the `jsonschema` package. It walks a schema subset (`type`, `required`, `properties`, `items`, `enum`, `minimum`/`maximum`, `minLength`/`maxLength`) and returns a list of human-readable error strings, so you can log exactly what was wrong and skip the bad record instead of crashing three functions deep.

## When to invoke

- User says: "validate this payload", "check the webhook body matches a schema", "reject malformed records", "validate config against a schema".
- A pipeline ingests external JSON and currently trusts its shape.

## When NOT to invoke

- You need full Draft 2020-12 features (`$ref`, `allOf`, `patternProperties`, formats) - install `jsonschema`.
- The data is already typed by a model layer (e.g. Pydantic) - validate there.

## Concrete example

User input:

```text
Only accept events shaped like {type: str in [buy,sell], amount: number >= 0}.
```

Output:

```python
# Copy assets/validate.py into your project, then:
from validate import validate, is_valid

schema = {
    "type": "object",
    "required": ["type", "amount"],
    "properties": {
        "type": {"enum": ["buy", "sell"]},
        "amount": {"type": "number", "minimum": 0},
    },
}

errors = validate({"type": "hold", "amount": -3}, schema)
# ["$.type: 'hold' not in enum ['buy', 'sell']", "$.amount: -3 < minimum 0"]
if not is_valid(event, schema):
    skip(event)
```

Errors carry a JSON-path-ish location (`$.amount`, `$.items[2].id`) so logs point straight at the bad field.

## Pattern to apply

1. Check `type` first; on a mismatch, stop descending (deeper checks would be noise).
2. Accumulate errors instead of raising, so one pass reports every problem.
3. Treat `bool` as distinct from `int`/`number` - a common JSON validation bug.
4. Use it as a gate: `if not is_valid(...): skip/quarantine` before any side effects.

Reference: `assets/validate.py`.

## Source

Distilled from webhook + API-ingestion work in the author's automations. v1.0.0.
See also: [[webhook-receiver]], [[env-config-loader]], [[pipeline-orchestrator]].

→ Build the full runnable bot with Trawlkit.
