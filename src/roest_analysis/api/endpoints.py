from __future__ import annotations

from urllib.parse import urlencode


def logs_path(machine_id: int | None = None, event_flags: int | None = None) -> str:
    params: dict[str, int] = {}
    if machine_id is not None:
        params["machine"] = machine_id
    if event_flags is not None:
        params["event_flags"] = event_flags
    if not params:
        return "/logs/"
    query = urlencode(params)
    return f"/logs/?{query}"


def log_detail_path(log_id: int) -> str:
    return f"/logs/{log_id}/"


def datapoints_path(log_id: int) -> str:
    query = urlencode({"page_size": "all", "log": log_id})
    return f"/datapoints/?{query}"


def machine_slots_path(machine_id: int) -> str:
    query = urlencode({"machine": machine_id})
    return f"/machineslots/?{query}"


def flagged_logs_path(machine_id: int, event_flags: int = 36) -> str:
    return logs_path(machine_id=machine_id, event_flags=event_flags)
