"""A tiny, dependency-free validator for a useful subset of JSON Schema.

Supports: ``type`` (object/array/string/number/integer/boolean/null), ``required``,
``properties``, ``items``, ``enum``, ``minimum``/``maximum``, ``minLength``/``maxLength``.
Returns a list of human-readable error strings (empty == valid). For full Draft
2020-12 coverage, use the ``jsonschema`` package instead.
"""

from __future__ import annotations

from typing import Any

_TYPES: dict[str, type | tuple[type, ...]] = {
    "object": dict,
    "array": list,
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "null": type(None),
}


def _type_ok(value: Any, expected: str) -> bool:
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    py = _TYPES.get(expected)
    return isinstance(value, py) if py is not None else True


def validate(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Return a list of validation errors; an empty list means ``value`` is valid."""
    errors: list[str] = []

    expected = schema.get("type")
    if expected and not _type_ok(value, expected):
        errors.append(f"{path}: expected {expected}, got {type(value).__name__}")
        return errors  # type mismatch makes deeper checks meaningless

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in enum {schema['enum']}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: {value} < minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: {value} > maximum {schema['maximum']}")

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: longer than maxLength {schema['maxLength']}")

    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required key '{key}'")
        for key, subschema in schema.get("properties", {}).items():
            if key in value:
                errors.extend(validate(value[key], subschema, f"{path}.{key}"))

    if isinstance(value, list) and "items" in schema:
        for index, element in enumerate(value):
            errors.extend(validate(element, schema["items"], f"{path}[{index}]"))

    return errors


def is_valid(value: Any, schema: dict[str, Any]) -> bool:
    return not validate(value, schema)
