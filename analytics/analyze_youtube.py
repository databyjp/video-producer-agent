#!/usr/bin/env python3
"""Analyze YouTube Studio daily CSV exports stored in ZIP archives."""

from __future__ import annotations

import argparse
import csv
import io
import re
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from statistics import median
from zipfile import BadZipFile, ZipFile


ARCHIVE_RE = re.compile(
    r"^Date (?P<start>\d{4}-\d{2}-\d{2})_(?P<end>\d{4}-\d{2}-\d{2}) "
    r"(?P<title>.+)\.zip$"
)
TABLE_NAME = "Table data.csv"

SUM_FIELDS = {
    "impressions": "Impressions",
    "subscribers_gained": "Subscribers gained",
    "subscribers_lost": "Subscribers lost",
    "likes": "Likes",
    "comments": "Comments added",
    "views": "Views",
    "watch_hours": "Watch time (hours)",
}


def number(value: str | None) -> float:
    if not value:
        return 0.0
    return float(value.replace(",", "").strip())


def duration_seconds(value: str | None) -> float:
    if not value:
        return 0.0
    parts = [int(part) for part in value.split(":")]
    if len(parts) == 3:
        hours, minutes, seconds = parts
    elif len(parts) == 2:
        hours, minutes, seconds = 0, *parts
    else:
        raise ValueError(f"Unexpected duration: {value!r}")
    return hours * 3600 + minutes * 60 + seconds


def format_duration(seconds: float) -> str:
    rounded = max(0, round(seconds))
    hours, remainder = divmod(rounded, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}"


@dataclass
class Export:
    title: str
    archive: Path
    export_start: date
    export_end: date
    first_activity: date
    left_censored: bool
    total: dict[str, str]
    daily: list[dict[str, str]]


def read_export(archive: Path) -> Export:
    match = ARCHIVE_RE.match(archive.name)
    if not match:
        raise ValueError(
            "Archive name does not match YouTube Studio's export pattern: "
            f"{archive.name}"
        )

    with ZipFile(archive) as zip_file:
        if TABLE_NAME not in zip_file.namelist():
            raise ValueError(f"{archive.name} does not contain {TABLE_NAME!r}")
        with zip_file.open(TABLE_NAME) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
            rows = list(csv.DictReader(text))

    total = next((row for row in rows if row["Date"] == "Total"), None)
    if total is None:
        raise ValueError(f"{archive.name} has no Total row")

    daily = [row for row in rows if row["Date"] != "Total"]
    daily.sort(key=lambda row: row["Date"])
    if not daily:
        raise ValueError(f"{archive.name} has no daily rows")

    export_start = date.fromisoformat(match.group("start"))
    export_end = date.fromisoformat(match.group("end"))
    first_activity = date.fromisoformat(daily[0]["Date"])

    return Export(
        title=match.group("title"),
        archive=archive,
        export_start=export_start,
        export_end=export_end,
        first_activity=first_activity,
        left_censored=first_activity == export_start,
        total=total,
        daily=daily,
    )


def aggregate_rows(rows: list[dict[str, str]]) -> dict[str, float]:
    result = {
        output_name: sum(number(row[column]) for row in rows)
        for output_name, column in SUM_FIELDS.items()
    }

    impressions = result["impressions"]
    views = result["views"]
    result["ctr_pct"] = (
        sum(
            number(row["Impressions"])
            * number(row["Impressions click-through rate (%)"])
            for row in rows
        )
        / impressions
        if impressions
        else 0.0
    )
    result["average_percentage_viewed_pct"] = (
        sum(
            number(row["Views"]) * number(row["Average percentage viewed (%)"])
            for row in rows
        )
        / views
        if views
        else 0.0
    )
    result["average_view_duration_seconds"] = (
        result["watch_hours"] * 3600 / views if views else 0.0
    )
    result["subscribers_per_1k_views"] = (
        result["subscribers_gained"] * 1000 / views if views else 0.0
    )
    result["likes_per_1k_views"] = result["likes"] * 1000 / views if views else 0.0
    result["comments_per_1k_views"] = (
        result["comments"] * 1000 / views if views else 0.0
    )
    return result


def aggregate_total(row: dict[str, str]) -> dict[str, float]:
    result = {
        output_name: number(row[column])
        for output_name, column in SUM_FIELDS.items()
    }
    result["ctr_pct"] = number(row["Impressions click-through rate (%)"])
    result["average_percentage_viewed_pct"] = number(
        row["Average percentage viewed (%)"]
    )
    result["average_view_duration_seconds"] = duration_seconds(
        row["Average view duration"]
    )
    views = result["views"]
    result["subscribers_per_1k_views"] = (
        result["subscribers_gained"] * 1000 / views if views else 0.0
    )
    result["likes_per_1k_views"] = result["likes"] * 1000 / views if views else 0.0
    result["comments_per_1k_views"] = (
        result["comments"] * 1000 / views if views else 0.0
    )
    return result


def window_metrics(export: Export, days: int) -> tuple[bool, dict[str, float]]:
    window_end = export.first_activity + timedelta(days=days - 1)
    rows = [
        row
        for row in export.daily
        if date.fromisoformat(row["Date"]) <= window_end
    ]
    complete = not export.left_censored and export.export_end >= window_end
    return complete, aggregate_rows(rows)


def build_summary(exports: list[Export], windows: list[int]) -> list[dict[str, object]]:
    summary: list[dict[str, object]] = []
    for export in exports:
        row: dict[str, object] = {
            "title": export.title,
            "archive": export.archive.name,
            "first_activity_date": export.first_activity.isoformat(),
            "publication_date_is_proxy": True,
            "left_censored": export.left_censored,
            "export_end_date": export.export_end.isoformat(),
        }

        for key, value in aggregate_total(export.total).items():
            row[f"lifetime_{key}"] = value

        for days in windows:
            complete, metrics = window_metrics(export, days)
            row[f"first_{days}d_complete"] = complete
            for key, value in metrics.items():
                row[f"first_{days}d_{key}"] = value

        summary.append(row)
    return summary


def write_summary_csv(rows: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            formatted = {}
            for key, value in row.items():
                if isinstance(value, float):
                    formatted[key] = f"{value:.4f}"
                else:
                    formatted[key] = value
            writer.writerow(formatted)


def markdown_table(
    rows: list[dict[str, object]],
    columns: list[tuple[str, str]],
    limit: int = 8,
) -> list[str]:
    lines = [
        "| " + " | ".join(label for _, label in columns) + " |",
        "|" + "|".join("---" for _ in columns) + "|",
    ]
    for row in rows[:limit]:
        values = []
        for key, _ in columns:
            value = row[key]
            if key.endswith("average_view_duration_seconds"):
                values.append(format_duration(float(value)))
            elif isinstance(value, float):
                values.append(f"{value:,.2f}")
            else:
                values.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
    return lines


def write_report(
    rows: list[dict[str, object]],
    output: Path,
    source: Path,
    windows: list[int],
) -> None:
    primary_window = 28 if 28 in windows else max(windows)
    prefix = f"first_{primary_window}d_"
    complete_rows = [
        row for row in rows if row[f"first_{primary_window}d_complete"]
    ]

    lines = [
        "# YouTube Analytics Summary",
        "",
        f"- Source: `{source}`",
        f"- Videos processed: {len(rows)}",
        (
            f"- Complete first-{primary_window}-day windows: "
            f"{len(complete_rows)} of {len(rows)}"
        ),
        (
            "- Publication date proxy: earliest exported day with activity. "
            "This is not guaranteed to be the actual publish timestamp."
        ),
        "",
        "## Lifetime overview",
        "",
    ]

    lifetime_ranked = sorted(
        rows, key=lambda row: float(row["lifetime_views"]), reverse=True
    )
    lines.extend(
        markdown_table(
            lifetime_ranked,
            [
                ("title", "Video"),
                ("lifetime_views", "Views"),
                ("lifetime_impressions", "Impressions"),
                ("lifetime_ctr_pct", "CTR %"),
                ("lifetime_average_percentage_viewed_pct", "Avg viewed %"),
                ("lifetime_subscribers_per_1k_views", "Subs/1K views"),
            ],
        )
    )

    lines.extend(["", f"## First {primary_window} days", ""])
    if not complete_rows:
        lines.append("No complete windows were available.")
    else:
        first_window_ranked = sorted(
            complete_rows,
            key=lambda row: float(row[f"{prefix}views"]),
            reverse=True,
        )
        lines.extend(
            markdown_table(
                first_window_ranked,
                [
                    ("title", "Video"),
                    (f"{prefix}views", "Views"),
                    (f"{prefix}impressions", "Impressions"),
                    (f"{prefix}ctr_pct", "CTR %"),
                    (f"{prefix}average_percentage_viewed_pct", "Avg viewed %"),
                    (f"{prefix}subscribers_per_1k_views", "Subs/1K views"),
                ],
            )
        )

        views_median = median(float(row[f"{prefix}views"]) for row in complete_rows)
        impressions_median = median(
            float(row[f"{prefix}impressions"]) for row in complete_rows
        )
        ctr_median = median(float(row[f"{prefix}ctr_pct"]) for row in complete_rows)
        viewed_median = median(
            float(row[f"{prefix}average_percentage_viewed_pct"])
            for row in complete_rows
        )

        packaging_candidates = sorted(
            (
                row
                for row in complete_rows
                if float(row[f"{prefix}impressions"]) >= impressions_median
                and float(row[f"{prefix}ctr_pct"]) < ctr_median
            ),
            key=lambda row: float(row[f"{prefix}impressions"]),
            reverse=True,
        )
        distribution_candidates = sorted(
            (
                row
                for row in complete_rows
                if float(row[f"{prefix}views"]) < views_median
                and float(row[f"{prefix}ctr_pct"]) >= ctr_median
                and float(row[f"{prefix}average_percentage_viewed_pct"])
                >= viewed_median
            ),
            key=lambda row: float(row[f"{prefix}ctr_pct"]),
            reverse=True,
        )

        lines.extend(
            [
                "",
                "## Descriptive review candidates",
                "",
                (
                    "These are prompts for human review, not causal findings. "
                    "The exports mix formats, audiences, video lengths, and traffic sources."
                ),
                "",
                (
                    f"- Dataset medians for complete first-{primary_window}-day windows: "
                    f"{views_median:,.0f} views, {impressions_median:,.0f} impressions, "
                    f"{ctr_median:.2f}% CTR, {viewed_median:.2f}% average viewed."
                ),
            ]
        )
        if packaging_candidates:
            names = "; ".join(str(row["title"]) for row in packaging_candidates[:5])
            lines.append(
                "- Packaging review candidates — above-median impressions but "
                f"below-median CTR: {names}."
            )
        if distribution_candidates:
            names = "; ".join(str(row["title"]) for row in distribution_candidates[:5])
            lines.append(
                "- Distribution/topic review candidates — below-median views despite "
                f"above-median CTR and retention: {names}."
            )

    lines.extend(
        [
            "",
            "## Interpretation limits",
            "",
            "- Daily exports provide calendar-day data, not a true rolling first 24 hours.",
            "- CTR only covers impressions on eligible YouTube surfaces.",
            "- Retention comparisons across videos of very different lengths are weak.",
            "- Traffic source and format should be added before drawing strategic conclusions.",
            "- Small differences should not be treated as meaningful without enough views.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Analyze zipped daily exports from YouTube Studio."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Directory containing YouTube Studio ZIP exports.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory (default: analytics/results/<input-directory>).",
    )
    parser.add_argument(
        "--windows",
        default="1,7,28",
        help="Comma-separated calendar-day windows (default: 1,7,28).",
    )
    args = parser.parse_args()
    args.input = args.input.expanduser().resolve()
    args.output = (
        args.output.expanduser().resolve()
        if args.output
        else script_dir / "results" / args.input.name
    )
    args.windows = sorted({int(value) for value in args.windows.split(",")})
    if not args.windows or any(value < 1 for value in args.windows):
        parser.error("--windows values must be positive integers")
    return args


def main() -> int:
    args = parse_args()
    archives = sorted(args.input.glob("*.zip"))
    if not archives:
        raise SystemExit(f"No ZIP exports found in {args.input}")

    exports = []
    errors = []
    for archive in archives:
        try:
            exports.append(read_export(archive))
        except (BadZipFile, KeyError, ValueError) as error:
            errors.append(f"{archive.name}: {error}")

    if not exports:
        raise SystemExit("No valid exports found:\n" + "\n".join(errors))

    rows = build_summary(exports, args.windows)
    args.output.mkdir(parents=True, exist_ok=True)
    write_summary_csv(rows, args.output / "video_summary.csv")
    write_report(
        rows,
        args.output / "report.md",
        source=args.input,
        windows=args.windows,
    )

    print(f"Processed {len(exports)} exports")
    print(f"Wrote {args.output / 'video_summary.csv'}")
    print(f"Wrote {args.output / 'report.md'}")
    if errors:
        print("\nSkipped exports:")
        for error in errors:
            print(f"- {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
