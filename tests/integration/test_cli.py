import json

from roest_analysis import cli


def test_doctor_config_masks_token(monkeypatch, capsys):
    class DummySettings:
        env_path = ".env"
        base_url = "https://api.roestcoffee.com"
        timeout_seconds = 30
        enable_live_tests = False
        machine_id = 9999
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
    assert payload["machine_id"] == 9999
    assert payload["token"] == "secr...oken"


def test_log_analyze_outputs_text(monkeypatch, capsys):
    class DummySettings:
        env_path = ".env"
        base_url = "https://api.roestcoffee.com"
        timeout_seconds = 30
        enable_live_tests = False
        machine_id = 9999
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


def test_machine_logs_uses_env_machine_id(monkeypatch, capsys):
    class DummySettings:
        env_path = ".env"
        base_url = "https://api.roestcoffee.com"
        timeout_seconds = 30
        enable_live_tests = False
        machine_id = 9999
        masked_token = "secr...oken"
        api_token = "secret-token"

    class DummyClient:
        def __init__(self, settings):
            self.settings = settings

        def get_logs(self, machine_id=None, event_flags=None):
            return {"machine_id": machine_id, "event_flags": event_flags}

    monkeypatch.setattr(cli, "load_settings", lambda: DummySettings())
    monkeypatch.setattr(cli, "RoestApiClient", DummyClient)

    exit_code = cli.main(["machine", "logs"])
    out = capsys.readouterr().out

    assert exit_code == 0
    payload = json.loads(out)
    assert payload["machine_id"] == 9999
