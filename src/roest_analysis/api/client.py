from __future__ import annotations

import json
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ..config import Settings
from ..errors import ApiError, NotFoundError
from . import endpoints
from .models import LogBundle


Transport = Callable[[Request, float], Any]


def _default_transport(request: Request, timeout: float):
    return urlopen(request, timeout=timeout)


class RoestApiClient:
    def __init__(self, settings: Settings, transport: Transport | None = None):
        self.settings = settings
        self.transport = transport or _default_transport

    def _request_json(self, path: str) -> Any:
        request = Request(
            f"{self.settings.base_url}{path}",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.settings.api_token}",
                "User-Agent": "roest-analysis/0.1.0",
            },
            method="GET",
        )
        try:
            with self.transport(request, self.settings.timeout_seconds) as response:
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            if exc.code == 404:
                raise NotFoundError(f"Roest resource not found: {path}") from exc
            raise ApiError(f"Roest API returned HTTP {exc.code} for {path}") from exc
        except URLError as exc:
            raise ApiError(f"Roest API request failed for {path}: {exc.reason}") from exc

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise ApiError(f"Roest API returned invalid JSON for {path}") from exc

    def get_log(self, log_id: int) -> dict[str, Any]:
        result = self._request_json(endpoints.log_detail_path(log_id))
        if not isinstance(result, dict):
            raise ApiError(f"Expected log detail object for log {log_id}")
        return result

    def get_datapoints(self, log_id: int) -> list[dict[str, Any]]:
        result = self._request_json(endpoints.datapoints_path(log_id))
        if not isinstance(result, list):
            raise ApiError(f"Expected datapoints array for log {log_id}")
        return result

    def get_machine_slots(self, machine_id: int) -> Any:
        return self._request_json(endpoints.machine_slots_path(machine_id))

    def get_logs(
        self,
        machine_id: int | None = None,
        event_flags: int | None = None,
    ) -> Any:
        return self._request_json(endpoints.logs_path(machine_id=machine_id, event_flags=event_flags))

    def get_flagged_logs(self, machine_id: int, event_flags: int = 36) -> Any:
        return self.get_logs(machine_id=machine_id, event_flags=event_flags)

    def get_log_bundle(self, log_id: int) -> LogBundle:
        return LogBundle(log=self.get_log(log_id), datapoints=self.get_datapoints(log_id))
