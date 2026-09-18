"""Run YOLO inference and optionally display the first annotated image."""

from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = PROJECT_ROOT / "runs/detect/models/trained/bitol_yolov8/weights/best.pt"
DEFAULT_SOURCE = PROJECT_ROOT / "detection_dataset/images/test"


def run_prediction(
    source: str | Path = DEFAULT_SOURCE,
    model_path: str | Path = DEFAULT_MODEL,
    confidence: float = 0.25,
    show: bool = True,
):
    """Run prediction, save annotated output, and display the first result."""
    source = Path(source).expanduser().resolve()
    model_path = Path(model_path).expanduser().resolve()

    if not model_path.is_file():
        raise FileNotFoundError(f"Model weights not found: {model_path}")
    if not source.exists():
        raise FileNotFoundError(f"Image source not found: {source}")

    model = YOLO(str(model_path))
    results = model.predict(
        source=str(source),
        save=True,
        conf=confidence,
        project=str(PROJECT_ROOT / "runs/detect"),
        name="predict",
    )

    if not results:
        print(f"No supported images were found in: {source}")
        return results

    output_dir = Path(results[0].save_dir)
    print(f"Annotated image(s) saved to: {output_dir}")

    if show:
        import matplotlib.pyplot as plt

        # result.plot() is BGR; Matplotlib expects RGB.
        annotated_rgb = results[0].plot()[..., ::-1]
        plt.figure(figsize=(12, 8))
        plt.imshow(annotated_rgb)
        plt.axis("off")
        plt.title(Path(results[0].path).name)
        plt.tight_layout()
        plt.show()

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", default=DEFAULT_SOURCE, help="Image, video, or directory")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Path to YOLO weights")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--no-show", action="store_true", help="Save without opening an image window")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_prediction(args.source, args.model, args.conf, show=not args.no_show)


if __name__ == "__main__":
    main()
