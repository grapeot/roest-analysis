from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from .errors import ConfigurationError


@dataclass(frozen=True)
class Settings:
    api_token: str
    base_url: str
    timeout_seconds: float
    enable_live_tests: bool
    env_path: Path

    @property
    def masked_token(self) -> str:
        token = self.api_token
        if len(token) <= 8:
            return "*" * len(token)
        return f"{token[:4]}...{token[-4:]}"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def load_settings(env_path: Path | None = None) -> Settings:
    resolved_env_path = env_path or project_root() / ".env"
    env_values = _parse_env_file(resolved_env_path)

    def get_value(key: str, default: str | None = None) -> str | None:
        return os.environ.get(key) or env_values.get(key) or default

    api_token = get_value("ROEST_API_TOKEN")
    if not api_token:
        raise ConfigurationError(
            f"Missing ROEST_API_TOKEN. Expected it in {resolved_env_path}."
        )

    base_url = get_value("ROEST_API_BASE_URL", "https://api.roestcoffee.com")
    if base_url is None:
        raise ConfigurationError("Missing ROEST_API_BASE_URL.")
    timeout = float(get_value("ROEST_HTTP_TIMEOUT", "30") or "30")
    enable_live_tests = (get_value("ROEST_ENABLE_LIVE_TESTS", "0") or "0") in {
        "1",
        "true",
        "TRUE",
        "yes",
        "YES",
    }
    return Settings(
        api_token=api_token,
        base_url=base_url.rstrip("/"),
        timeout_seconds=timeout,
        enable_live_tests=enable_live_tests,
        env_path=resolved_env_path,
    )
