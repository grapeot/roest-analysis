from pathlib import Path

import pytest

from roest_analysis.config import load_settings
from roest_analysis.errors import ConfigurationError


def test_load_settings_reads_env_file(tmp_path: Path):
    env_path = tmp_path / ".env"
    env_path.write_text(
        "ROEST_API_TOKEN=secret-token\nROEST_API_BASE_URL=https://example.com\nROEST_HTTP_TIMEOUT=12\n"
    )

    settings = load_settings(env_path=env_path)

    assert settings.api_token == "secret-token"
    assert settings.base_url == "https://example.com"
    assert settings.timeout_seconds == 12.0
    assert settings.machine_id is None
    assert settings.masked_token == "secr...oken"


def test_load_settings_reads_machine_id(tmp_path: Path):
    env_path = tmp_path / ".env"
    env_path.write_text("ROEST_API_TOKEN=secret-token\nROEST_MACHINE_ID=9999\n")

    settings = load_settings(env_path=env_path)

    assert settings.machine_id == 9999


def test_load_settings_requires_token(tmp_path: Path):
    env_path = tmp_path / ".env"
    env_path.write_text("ROEST_HTTP_TIMEOUT=12\n")

    with pytest.raises(ConfigurationError):
        load_settings(env_path=env_path)
