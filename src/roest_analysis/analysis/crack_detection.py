from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CrackPoint:
    time_s: float
    bt: float | None
    crack_level: int


@dataclass(frozen=True)
class CrackCluster:
    points: tuple[CrackPoint, ...]

    @property
    def start_time_s(self) -> float:
        return self.points[0].time_s

    @property
    def end_time_s(self) -> float:
        return self.points[-1].time_s

    @property
    def duration_s(self) -> float:
        return self.end_time_s - self.start_time_s

    @property
    def point_count(self) -> int:
        return len(self.points)

    @property
    def max_level(self) -> int:
        return max(point.crack_level for point in self.points)

    @property
    def start_bt(self) -> float | None:
        return self.points[0].bt


def _to_time_seconds(point: dict[str, Any]) -> float | None:
    raw = point.get("msec", point.get("ms", point.get("time")))
    if raw is None:
        return None
    return float(raw) / 1000.0


def crack_points_from_datapoints(datapoints: list[dict[str, Any]]) -> list[CrackPoint]:
    points: list[CrackPoint] = []
    for point in datapoints:
        crack = point.get("crack") or 0
        if crack <= 0:
            continue
        time_s = _to_time_seconds(point)
        if time_s is None:
            continue
        bt = point.get("bt", point.get("bean_temp", point.get("beanTemperature")))
        points.append(CrackPoint(time_s=time_s, bt=bt, crack_level=int(crack)))
    return points


def build_clusters(points: list[CrackPoint], max_gap_s: float = 6.0) -> list[CrackCluster]:
    if not points:
        return []
    ordered = sorted(points, key=lambda point: point.time_s)
    clusters: list[list[CrackPoint]] = [[ordered[0]]]
    for point in ordered[1:]:
        if point.time_s - clusters[-1][-1].time_s <= max_gap_s:
            clusters[-1].append(point)
        else:
            clusters.append([point])
    return [CrackCluster(tuple(cluster)) for cluster in clusters]


def _cluster_score(cluster: CrackCluster) -> tuple[int, int, float, float]:
    return (
        cluster.point_count,
        cluster.max_level,
        cluster.duration_s,
        cluster.start_time_s,
    )


def analyze_crack_signal(datapoints: list[dict[str, Any]]) -> dict[str, Any]:
    points = crack_points_from_datapoints(datapoints)
    clusters = build_clusters(points)
    if not clusters:
        return {
            "points": [],
            "clusters": [],
            "practical_onset": None,
            "active_onset": None,
            "outlier_points": [],
            "ambiguous": True,
            "notes": ["No crack points detected."],
        }

    ranked_clusters = sorted(clusters, key=_cluster_score, reverse=True)
    best_cluster = ranked_clusters[0]
    practical_cluster = None
    outlier_points: list[dict[str, Any]] = []
    for cluster in clusters:
        if cluster.point_count >= 2 or cluster.max_level >= 2:
            practical_cluster = cluster
            break
        outlier_points.extend(
            {
                "time_s": point.time_s,
                "bt": point.bt,
                "crack_level": point.crack_level,
            }
            for point in cluster.points
        )

    if practical_cluster is None:
        practical_cluster = best_cluster

    ambiguity = False
    if len(ranked_clusters) > 1:
        runner_up = ranked_clusters[1]
        ambiguity = (
            runner_up.point_count >= best_cluster.point_count
            and runner_up.max_level >= best_cluster.max_level
        )

    if practical_cluster != best_cluster:
        delayed_active = best_cluster.start_time_s - practical_cluster.start_time_s
        stronger_active = (
            best_cluster.point_count > practical_cluster.point_count
            or best_cluster.max_level > practical_cluster.max_level
        )
        if delayed_active >= 12 and stronger_active:
            ambiguity = True

    notes = []
    if outlier_points:
        notes.append(
            "Early isolated crack points were treated as outliers before selecting practical onset."
        )
    if ambiguity:
        notes.append("Multiple crack clusters look similarly strong. Review the full sequence.")
    if practical_cluster != best_cluster:
        notes.append(
            "Practical onset and active crack cluster diverge; interpret development conservatively."
        )

    return {
        "points": [
            {"time_s": point.time_s, "bt": point.bt, "crack_level": point.crack_level}
            for point in points
        ],
        "clusters": [
            {
                "start_time_s": cluster.start_time_s,
                "end_time_s": cluster.end_time_s,
                "point_count": cluster.point_count,
                "max_level": cluster.max_level,
                "start_bt": cluster.start_bt,
            }
            for cluster in clusters
        ],
        "practical_onset": {
            "time_s": practical_cluster.start_time_s,
            "bt": practical_cluster.start_bt,
            "point_count": practical_cluster.point_count,
            "max_level": practical_cluster.max_level,
        },
        "active_onset": {
            "time_s": best_cluster.start_time_s,
            "bt": best_cluster.start_bt,
            "point_count": best_cluster.point_count,
            "max_level": best_cluster.max_level,
        },
        "outlier_points": outlier_points,
        "ambiguous": ambiguity,
        "notes": notes,
    }
