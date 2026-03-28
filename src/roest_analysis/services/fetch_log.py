from __future__ import annotations

from ..api.client import RoestApiClient
from ..api.models import LogBundle


def fetch_log_bundle(client: RoestApiClient, log_id: int) -> LogBundle:
    return client.get_log_bundle(log_id)
