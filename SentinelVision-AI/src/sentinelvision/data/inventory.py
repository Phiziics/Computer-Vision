from pathlib import Path

import cv2
import pandas as pd
from tqdm import tqdm


ANOMALY_CATEGORIES = (
    "Abuse",
    "Arrest",
    "Arson",
    "Assault",
    "Burglary",
    "Explosion",
    "Fighting",
    "RoadAccidents",
    "Robbery",
    "Shooting",
    "Shoplifting",
    "Stealing",
    "Vandalism",
)


def find_video_files(
    raw_dir: str | Path,
    allowed_extensions: list[str],
) -> list[Path]:
    """
    Recursively find supported video files.
    """
    raw_path = Path(raw_dir)

    valid_extensions = {
        extension.lower()
        for extension in allowed_extensions
    }

    video_files = [
        path
        for path in raw_path.rglob("*")
        if path.is_file()
        and path.suffix.lower() in valid_extensions
    ]

    return sorted(video_files)


def infer_category(video_path: Path) -> str:
    """
    Infer UCF-Crime category from the file name.

    Examples:
        Abuse001_x264.mp4 -> Abuse
        Robbery025_x264.mp4 -> Robbery
        Normal_Videos_015_x264.mp4 -> Normal
    """
    file_name = video_path.stem

    # Normal videos usually contain "Normal" in the file name.
    if "normal" in file_name.lower():
        return "Normal"

    # Match known anomaly categories.
    for category in ANOMALY_CATEGORIES:
        if file_name.lower().startswith(category.lower()):
            return category

    return "Unknown"


def infer_binary_label(category: str) -> int:
    """
    Convert category into a binary anomaly label.

    0 = normal
    1 = anomalous
    """
    return 0 if category == "Normal" else 1


def inspect_video(
    video_path: Path,
    raw_dir: str | Path,
) -> dict:
    """
    Extract technical metadata from one video.
    """
    raw_path = Path(raw_dir)

    capture = cv2.VideoCapture(str(video_path))

    is_readable = capture.isOpened()

    fps = 0.0
    frame_count = 0
    width = 0
    height = 0
    duration_seconds = 0.0

    if is_readable:
        fps = float(
            capture.get(cv2.CAP_PROP_FPS)
        )

        frame_count = int(
            capture.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        width = int(
            capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        if fps > 0:
            duration_seconds = frame_count / fps

    capture.release()

    category = infer_category(video_path)

    binary_label = infer_binary_label(category)

    try:
        relative_path = video_path.relative_to(raw_path)
    except ValueError:
        relative_path = video_path

    return {
        "video_id": video_path.stem,
        "file_name": video_path.name,
        "file_path": str(video_path),
        "relative_path": str(relative_path),
        "parent_folder": video_path.parent.name,
        "category": category,
        "binary_label": binary_label,
        "file_extension": video_path.suffix.lower(),
        "file_size_mb": round(
            video_path.stat().st_size / (1024**2),
            3,
        ),
        "is_readable": is_readable,
        "fps": round(fps, 3),
        "frame_count": frame_count,
        "width": width,
        "height": height,
        "duration_seconds": round(
            duration_seconds,
            3,
        ),
        "duration_minutes": round(
            duration_seconds / 60,
            3,
        ),
    }


def build_video_inventory(
    raw_dir: str | Path,
    allowed_extensions: list[str],
) -> pd.DataFrame:
    """
    Build a metadata inventory for all discovered videos.
    """
    video_files = find_video_files(
        raw_dir=raw_dir,
        allowed_extensions=allowed_extensions,
    )

    if not video_files:
        return pd.DataFrame()

    records = []

    for video_path in tqdm(
        video_files,
        desc="Inspecting videos",
    ):
        record = inspect_video(
            video_path=video_path,
            raw_dir=raw_dir,
        )

        records.append(record)

    inventory = pd.DataFrame(records)

    return inventory