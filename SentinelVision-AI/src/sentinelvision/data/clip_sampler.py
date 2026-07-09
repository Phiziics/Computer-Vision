from pathlib import Path

import pandas as pd
from tqdm import tqdm


def generate_clip_windows(
    duration_seconds: float,
    clip_duration_seconds: float,
    stride_seconds: float,
    minimum_clip_seconds: float = 2.0,
    include_partial_final_clip: bool = False,
) -> list[tuple[float, float]]:
    """
    Generate temporal clip windows for one source video.

    Returns
    -------
    list[tuple[float, float]]
        List of (start_seconds, end_seconds) windows.
    """
    if duration_seconds <= 0:
        return []

    if clip_duration_seconds <= 0:
        raise ValueError(
            "clip_duration_seconds must be greater than 0."
        )

    if stride_seconds <= 0:
        raise ValueError(
            "stride_seconds must be greater than 0."
        )

    windows = []

    start_seconds = 0.0

    while start_seconds < duration_seconds:
        end_seconds = start_seconds + clip_duration_seconds

        # Full clip fits inside the source video.
        if end_seconds <= duration_seconds:
            windows.append(
                (
                    round(start_seconds, 3),
                    round(end_seconds, 3),
                )
            )

        else:
            remaining_seconds = (
                duration_seconds - start_seconds
            )

            # Optionally preserve a sufficiently long
            # partial clip at the end.
            if (
                include_partial_final_clip
                and remaining_seconds >= minimum_clip_seconds
            ):
                windows.append(
                    (
                        round(start_seconds, 3),
                        round(duration_seconds, 3),
                    )
                )

            break

        start_seconds += stride_seconds

    return windows


def build_clip_manifest(
    video_splits: pd.DataFrame,
    clip_duration_seconds: float,
    stride_seconds: float,
    minimum_clip_seconds: float = 2.0,
    include_partial_final_clip: bool = False,
) -> pd.DataFrame:
    """
    Build a clip-level manifest from the frozen
    source-video split manifest.

    Each clip inherits the split of its source video.
    """
    required_columns = {
        "video_id",
        "file_path",
        "category",
        "binary_label",
        "split",
        "duration_seconds",
        "fps",
    }

    missing_columns = required_columns.difference(
        video_splits.columns
    )

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{sorted(missing_columns)}"
        )

    records = []

    for row in tqdm(
        video_splits.itertuples(index=False),
        total=len(video_splits),
        desc="Building clip manifest",
    ):
        windows = generate_clip_windows(
            duration_seconds=float(
                row.duration_seconds
            ),
            clip_duration_seconds=clip_duration_seconds,
            stride_seconds=stride_seconds,
            minimum_clip_seconds=minimum_clip_seconds,
            include_partial_final_clip=(
                include_partial_final_clip
            ),
        )

        for clip_index, (
            start_seconds,
            end_seconds,
        ) in enumerate(windows):
            clip_id = (
                f"{row.video_id}_clip_{clip_index:05d}"
            )

            records.append(
                {
                    "clip_id": clip_id,
                    "video_id": row.video_id,
                    "file_path": row.file_path,
                    "category": row.category,
                    "binary_label": row.binary_label,
                    "split": row.split,
                    "clip_index": clip_index,
                    "start_seconds": start_seconds,
                    "end_seconds": end_seconds,
                    "clip_duration_seconds": round(
                        end_seconds - start_seconds,
                        3,
                    ),
                    "source_video_duration_seconds": (
                        row.duration_seconds
                    ),
                    "source_fps": row.fps,
                }
            )

    return pd.DataFrame(records)


def validate_clip_manifest(
    clip_manifest: pd.DataFrame,
    video_splits: pd.DataFrame,
) -> dict[str, bool]:
    """
    Verify that clip creation preserved
    source-video split assignments.
    """
    if clip_manifest.empty:
        return {
            "manifest_not_empty": False,
            "unique_clip_ids": False,
            "no_cross_split_video_leakage": False,
            "split_matches_source_video": False,
        }

    unique_clip_ids = (
        not clip_manifest["clip_id"]
        .duplicated()
        .any()
    )

    # One source video must still appear
    # in exactly one split.
    no_cross_split_video_leakage = (
        clip_manifest
        .groupby("video_id")["split"]
        .nunique()
        .max()
        == 1
    )

    # Build authoritative video_id -> split mapping.
    source_split_map = (
        video_splits
        .set_index("video_id")["split"]
        .to_dict()
    )

    expected_splits = (
        clip_manifest["video_id"]
        .map(source_split_map)
    )

    split_matches_source_video = (
        expected_splits
        .eq(clip_manifest["split"])
        .all()
    )

    return {
        "manifest_not_empty": True,
        "unique_clip_ids": unique_clip_ids,
        "no_cross_split_video_leakage": (
            no_cross_split_video_leakage
        ),
        "split_matches_source_video": (
            split_matches_source_video
        ),
    }


def save_clip_manifest(
    clip_manifest: pd.DataFrame,
    output_dir: str | Path,
) -> tuple[Path, Path]:
    """
    Save clip metadata as CSV and Parquet.
    """
    output_path = Path(output_dir)

    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_path = (
        output_path / "clip_manifest.csv"
    )

    parquet_path = (
        output_path / "clip_manifest.parquet"
    )

    clip_manifest.to_csv(
        csv_path,
        index=False,
    )

    clip_manifest.to_parquet(
        parquet_path,
        index=False,
    )

    return csv_path, parquet_path