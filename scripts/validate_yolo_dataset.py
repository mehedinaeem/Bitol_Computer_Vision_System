#!/usr/bin/env python3
"""Validate a YOLO detection dataset and write a detailed CSV report."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


SPLITS = ("train", "val", "test")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
CRITICAL_CATEGORIES = {
    "missing_label",
    "orphan_label",
    "empty_label",
    "malformed_row",
    "invalid_class_id",
    "invalid_coordinate",
    "duplicate_row",
    "git_conflict_marker",
}


@dataclass
class Stats:
    images: int = 0
    labels: int = 0
    missing_labels: int = 0
    orphan_labels: int = 0
    empty_labels: int = 0
    malformed_rows: int = 0
    invalid_class_ids: int = 0
    invalid_coordinates: int = 0
    duplicate_rows: int = 0
    conflict_markers: int = 0
    healthy_instances: int = 0
    unhealthy_instances: int = 0
    total_boxes: int = 0
    issues: list[dict[str, str | int]] = field(default_factory=list)

    def add_issue(self, category: str, path: Path, line: int | str = "", details: str = "") -> None:
        self.issues.append({
            "split": "",
            "category": category,
            "path": path.as_posix(),
            "line": line,
            "details": details,
        })


def index_images(directory: Path) -> dict[str, list[Path]]:
    result: dict[str, list[Path]] = {}
    if not directory.exists():
        return result
    for path in directory.iterdir():
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            result.setdefault(path.stem, []).append(path)
    return result


def validate_split(dataset: Path, split: str) -> Stats:
    stats = Stats()
    images = index_images(dataset / "images" / split)
    label_dir = dataset / "labels" / split
    labels = {
        path.stem: path
        for path in label_dir.glob("*.txt")
        if path.name != "classes.txt"
    } if label_dir.exists() else {}
    stats.images = sum(len(paths) for paths in images.values())
    stats.labels = len(labels)

    for stem in sorted(images.keys() - labels.keys()):
        for image in images[stem]:
            stats.missing_labels += 1
            stats.add_issue("missing_label", image, details="No label with the same stem")
    for stem in sorted(labels.keys() - images.keys()):
        stats.orphan_labels += 1
        stats.add_issue("orphan_label", labels[stem], details="No image with the same stem")
    for stem, paths in sorted(images.items()):
        if len(paths) > 1:
            stats.add_issue("duplicate_image_stem", paths[0], details=", ".join(p.as_posix() for p in paths))

    for label in sorted(labels.values()):
        lines = label.read_text(encoding="utf-8", errors="replace").splitlines()
        nonempty = [(number, line.strip()) for number, line in enumerate(lines, 1) if line.strip()]
        if not nonempty:
            stats.empty_labels += 1
            stats.add_issue("empty_label", label, details="Zero non-empty annotation rows")
            continue

        marker_rows = [(number, row) for number, row in nonempty if row.startswith(CONFLICT_MARKERS)]
        if marker_rows:
            for line_number, row in marker_rows:
                stats.conflict_markers += 1
                stats.add_issue("git_conflict_marker", label, line_number, row)
            # Do not treat either unresolved alternative as active annotations.
            continue

        row_counts = Counter(line for _, line in nonempty)
        for row, count in sorted(row_counts.items()):
            if count > 1:
                stats.duplicate_rows += count - 1
                stats.add_issue("duplicate_row", label, details=f"Repeated {count} times: {row}")

        for line_number, row in nonempty:
            fields = row.split()
            if len(fields) != 5:
                stats.malformed_rows += 1
                stats.add_issue("malformed_row", label, line_number, f"Expected 5 fields: {row}")
                continue
            try:
                class_value = float(fields[0])
                coordinates = [float(value) for value in fields[1:]]
            except ValueError:
                stats.malformed_rows += 1
                stats.add_issue("malformed_row", label, line_number, f"Non-numeric field: {row}")
                continue
            if not math.isfinite(class_value) or any(not math.isfinite(value) for value in coordinates):
                stats.malformed_rows += 1
                stats.add_issue("malformed_row", label, line_number, f"Non-finite value: {row}")
                continue

            class_id = int(class_value)
            valid_class = class_value == class_id and class_id in (0, 1)
            if not valid_class:
                stats.invalid_class_ids += 1
                stats.add_issue("invalid_class_id", label, line_number, f"Class must be 0 or 1: {fields[0]}")

            x_center, y_center, width, height = coordinates
            coordinate_errors = []
            if not 0 <= x_center <= 1: coordinate_errors.append("x_center outside [0,1]")
            if not 0 <= y_center <= 1: coordinate_errors.append("y_center outside [0,1]")
            if not 0 < width <= 1: coordinate_errors.append("width outside (0,1]")
            if not 0 < height <= 1: coordinate_errors.append("height outside (0,1]")
            if x_center - width / 2 < 0: coordinate_errors.append("left edge < 0")
            if x_center + width / 2 > 1: coordinate_errors.append("right edge > 1")
            if y_center - height / 2 < 0: coordinate_errors.append("top edge < 0")
            if y_center + height / 2 > 1: coordinate_errors.append("bottom edge > 1")
            if coordinate_errors:
                stats.invalid_coordinates += 1
                stats.add_issue("invalid_coordinate", label, line_number, "; ".join(coordinate_errors) + f": {row}")

            if valid_class:
                stats.healthy_instances += class_id == 0
                stats.unhealthy_instances += class_id == 1
                stats.total_boxes += 1
    for issue in stats.issues:
        issue["split"] = split
    return stats


def total_stats(results: dict[str, Stats]) -> Stats:
    total = Stats()
    for stats in results.values():
        for name in (
            "images", "labels", "missing_labels", "orphan_labels", "empty_labels",
            "malformed_rows", "invalid_class_ids", "invalid_coordinates", "duplicate_rows",
            "conflict_markers", "healthy_instances", "unhealthy_instances", "total_boxes",
        ):
            setattr(total, name, getattr(total, name) + getattr(stats, name))
        total.issues.extend(stats.issues)
    return total


def print_stats(name: str, stats: Stats) -> None:
    print(f"\n{name}")
    print(f"  Images: {stats.images}")
    print(f"  Labels: {stats.labels}")
    print(f"  Missing labels: {stats.missing_labels}")
    print(f"  Orphan labels: {stats.orphan_labels}")
    print(f"  Empty labels: {stats.empty_labels}")
    print(f"  Malformed rows: {stats.malformed_rows}")
    print(f"  Invalid class IDs: {stats.invalid_class_ids}")
    print(f"  Invalid coordinates: {stats.invalid_coordinates}")
    print(f"  Duplicate annotation rows: {stats.duplicate_rows}")
    print(f"  Git conflict markers: {stats.conflict_markers}")
    print(f"  Healthy instances: {stats.healthy_instances}")
    print(f"  Unhealthy instances: {stats.unhealthy_instances}")
    print(f"  Total bounding boxes: {stats.total_boxes}")


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=repository / "detection_dataset")
    parser.add_argument("--report", type=Path, default=repository / "dataset_validation_report.csv")
    args = parser.parse_args()
    dataset = args.dataset.resolve()
    if not dataset.is_dir():
        parser.error(f"Dataset directory does not exist: {dataset}")

    results = {split: validate_split(dataset, split) for split in SPLITS}
    total = total_stats(results)
    for split in SPLITS:
        print_stats(split, results[split])
    print_stats("TOTAL", total)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("split", "category", "path", "line", "details"))
        writer.writeheader()
        writer.writerows(total.issues)
    print(f"\nDetailed report: {args.report.resolve()}")

    critical = sum(1 for issue in total.issues if issue["category"] in CRITICAL_CATEGORIES)
    if critical:
        print(f"Validation failed: {critical} critical issue records remain.", file=sys.stderr)
        return 1
    print("Validation passed: no critical annotation errors found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
