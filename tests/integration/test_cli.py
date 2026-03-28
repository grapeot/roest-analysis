import json

from roest_analysis import cli


def test_doctor_config_masks_token(monkeypatch, capsys):
    class DummySettings:
        env_path = ".env"
        base_url = "https://api.roestcoffee.com"
        timeout_seconds = 30
        enable_live_tests = False
        masked_token = "secr...oken"
        api_token = "secret-token"

    class DummyClient:
        def __init__(self, settings):
            self.settings = settings

    monkeypatch.setattr(cli, "load_settings", lambda: DummySettings())
    monkeypatch.setattr(cli, "RoestApiClient", DummyClient)

    exit_code = cli.main(["doctor", "config"])
    out = capsys.readouterr().out

    assert exit_code == 0
    payload = json.loads(out)
    assert payload["token"] == "secr...oken"


def test_log_analyze_outputs_text(monkeypatch, capsys):
    class DummySettings:
        env_path = ".env"
        base_url = "https://api.roestcoffee.com"
        timeout_seconds = 30
        enable_live_tests = False
        masked_token = "secr...oken"
        api_token = "secret-token"

    class DummyClient:
        def __init__(self, settings):
            self.settings = settings

    monkeypatch.setattr(cli, "load_settings", lambda: DummySettings())
    monkeypatch.setattr(cli, "RoestApiClient", DummyClient)
    monkeypatch.setattr(
        cli,
        "analyze_log_id",
        lambda client, log_id: {"summary_text": f"Log ID: {log_id}"},
    )

    exit_code = cli.main(["log", "analyze", "--log-id", "123"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert out.strip() == "Log ID: 123"
