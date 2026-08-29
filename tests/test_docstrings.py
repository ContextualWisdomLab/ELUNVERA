"""Ensure every shipped public Python symbol explains its contract."""

from __future__ import annotations

import inspect
from types import ModuleType
from typing import Any

from elunvera import queue
from scripts import serve


def public_symbols(module: ModuleType) -> list[tuple[str, Any]]:
    symbols: list[tuple[str, Any]] = []
    for name, value in vars(module).items():
        if name.startswith("_") or getattr(value, "__module__", None) != module.__name__:
            continue
        if inspect.isfunction(value) or inspect.isclass(value):
            symbols.append((f"{module.__name__}.{name}", value))
        if inspect.isclass(value):
            for member_name, member in vars(value).items():
                if member_name.startswith("_"):
                    continue
                if inspect.isfunction(member) or isinstance(member, property):
                    symbols.append((f"{module.__name__}.{name}.{member_name}", member))
    return symbols


def test_public_python_symbols_have_docstrings() -> None:
    missing = [
        name
        for module in (queue, serve)
        for name, symbol in public_symbols(module)
        if not inspect.getdoc(symbol)
    ]
    assert missing == []
