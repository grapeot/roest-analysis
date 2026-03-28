from __future__ import annotations

import argparse
import json
import sys

from .api.client import RoestApiClient
from .config import load_settings
from .errors import ConfigurationError, RoestAnalysisError
from .services.analyze_log import analyze_log_id


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="roest")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor")
    doctor_subparsers = doctor.add_subparsers(dest="doctor_command", required=True)
    doctor_subparsers.add_parser("config")

    log_parser = subparsers.add_parser("log")
    log_subparsers = log_parser.add_subparsers(dest="log_command", required=True)

    fetch_parser = log_subparsers.add_parser("fetch")
    fetch_parser.add_argument("--log-id", type=int, required=True)
    fetch_parser.add_argument(
        "--resource",
        choices=["log", "datapoints", "bundle"],
        default="bundle",
    )
    fetch_parser.add_argument("--format", choices=["json"], default="json")

    analyze_parser = log_subparsers.add_parser("analyze")
    analyze_parser.add_argument("--log-id", type=int, required=True)
    analyze_parser.add_argument("--format", choices=["text", "json"], default="text")

    machine_parser = subparsers.add_parser("machine")
    machine_subparsers = machine_parser.add_subparsers(dest="machine_command", required=True)

    logs = machine_subparsers.add_parser("logs")
    logs.add_argument("--machine-id", type=int)
    logs.add_argument("--event-flags", type=int)

    slots = machine_subparsers.add_parser("slots")
    slots.add_argument("--machine-id", type=int, required=True)

    flagged = machine_subparsers.add_parser("flagged-logs")
    flagged.add_argument("--machine-id", type=int, required=True)
    flagged.add_argument("--event-flags", type=int, default=36)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        settings = load_settings()
        client = RoestApiClient(settings)

        if args.command == "doctor" and args.doctor_command == "config":
            payload = {
                "env_path": str(settings.env_path),
                "base_url": settings.base_url,
                "timeout_seconds": settings.timeout_seconds,
                "enable_live_tests": settings.enable_live_tests,
                "token": settings.masked_token,
            }
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 0

        if args.command == "log" and args.log_command == "fetch":
            if args.resource == "log":
                payload = client.get_log(args.log_id)
            elif args.resource == "datapoints":
                payload = client.get_datapoints(args.log_id)
            else:
                bundle = client.get_log_bundle(args.log_id)
                payload = {"log": bundle.log, "datapoints": bundle.datapoints}
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 0

        if args.command == "log" and args.log_command == "analyze":
            result = analyze_log_id(client, args.log_id)
            if args.format == "json":
                print(json.dumps(result, indent=2, sort_keys=True))
            else:
                print(result["summary_text"])
            return 0

        if args.command == "machine" and args.machine_command == "slots":
            print(json.dumps(client.get_machine_slots(args.machine_id), indent=2, sort_keys=True))
            return 0

        if args.command == "machine" and args.machine_command == "logs":
            print(
                json.dumps(
                    client.get_logs(machine_id=args.machine_id, event_flags=args.event_flags),
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0

        if args.command == "machine" and args.machine_command == "flagged-logs":
            print(
                json.dumps(
                    client.get_flagged_logs(args.machine_id, args.event_flags),
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
    except (ConfigurationError, RoestAnalysisError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    parser.error("Unhandled command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
