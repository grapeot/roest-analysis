from pathlib import Path

from roest_analysis import cli


def test_log_plot_writes_svg(monkeypatch, tmp_path: Path):
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

    def fake_plot_log_id(client, log_id, output_path, title=None):
        output_path.write_text(f"<svg><text>{log_id}</text><text>{title}</text></svg>")
        return {"output_path": str(output_path)}

    monkeypatch.setattr(cli, "load_settings", lambda: DummySettings())
    monkeypatch.setattr(cli, "RoestApiClient", DummyClient)
    monkeypatch.setattr(cli, "plot_log_id", fake_plot_log_id)

    output = tmp_path / "roast.svg"
    exit_code = cli.main([
        "log",
        "plot",
        "--log-id",
        "123",
        "--output",
        str(output),
        "--title",
        "Example",
    ])

    assert exit_code == 0
    assert output.exists()
    assert "Example" in output.read_text()
