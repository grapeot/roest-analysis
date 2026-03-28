import json
from pathlib import Path

from roest_analysis.api.client import RoestApiClient
from roest_analysis.config import Settings


class DummyResponse:
    def __init__(self, payload):
        self.payload = payload

    def read(self):
        return json.dumps(self.payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_api_client_formats_known_endpoints():
    seen = []

    def transport(request, timeout):
        seen.append((request.full_url, request.headers, timeout))
        if "/datapoints/" in request.full_url:
            return DummyResponse([])
        return DummyResponse({"id": 123})

    settings = Settings(
        api_token="secret-token",
        base_url="https://api.roestcoffee.com",
        timeout_seconds=12.0,
        enable_live_tests=False,
        env_path=Path(".env"),
    )

    client = RoestApiClient(settings, transport=transport)
    bundle = client.get_log_bundle(123)
    client.get_logs(machine_id=2559)
    client.get_machine_slots(2559)
    client.get_flagged_logs(2559, 36)

    assert bundle.log["id"] == 123
    assert bundle.datapoints == []
    assert seen[0][0].endswith("/logs/123/")
    assert seen[1][0].endswith("/datapoints/?page_size=all&log=123")
    assert seen[2][0].endswith("/logs/?machine=2559")
    assert seen[3][0].endswith("/machineslots/?machine=2559")
    assert seen[4][0].endswith("/logs/?machine=2559&event_flags=36")
    assert seen[0][1]["Authorization"] == "Bearer secret-token"
