from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LogBundle:
    log: dict[str, Any]
    datapoints: list[dict[str, Any]]
