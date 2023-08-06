from typing import Any, Type


def is_string(value: Any) -> bool:
    return isinstance(value, str)


def is_float(value: Any) -> bool:
    return isinstance(value, float)


def is_list(value: Any) -> bool:
    return isinstance(value, list)


def is_list_of(value: Any, type: Type) -> bool:
    checks = [isinstance(v, type) for v in value]
    return is_list(value) and len(value) == sum(checks)
