from pathlib import Path

import pandas as pd

from sentinelvision.data.clip_sampler import (
    build_clip_manifest,
    save_clip_manifest,
    validate_clip_manifest,
)
from sentinelvision.utils.config import load_config


def main() -> None:
    """
    Build a leakage-safe temporal clip manifest.
    """
    config = load_config(
        "configs/data.yaml"
    )

    metadata_dir = Path(
        config["data"]["metadata_dir"]
    )

    split_path = (
        metadata_dir
        / "video_splits.parquet"
    )

    if not split_path.exists():
        raise FileNotFoundError(
            "Video split manifest not found. "
            "Run python scripts/create_splits.py first."
        )

    video_splits = pd.read_parquet(
        split_path
    )

    clip_config = config["clips"]

    clip_manifest = build_clip_manifest(
        video_splits=video_splits,
        clip_duration_seconds=clip_config[
            "duration_seconds"
        ],
        stride_seconds=clip_config[
            "stride_seconds"
        ],
        minimum_clip_seconds=clip_config[
            "minimum_clip_seconds"
        ],
        include_partial_final_clip=clip_config[
            "include_partial_final_clip"
        ],
    )

    integrity_results = validate_clip_manifest(
        clip_manifest=clip_manifest,
        video_splits=video_splits,
    )

    if not all(integrity_results.values()):
        raise RuntimeError(
            "Clip manifest integrity failed: "
            f"{integrity_results}"
        )

    csv_path, parquet_path = save_clip_manifest(
        clip_manifest=clip_manifest,
        output_dir=metadata_dir,
    )

    print("Clip manifest creation complete.")
    print()

    print("Integrity checks:")

    for check_name, passed in (
        integrity_results.items()
    ):
        print(
            f"  {check_name}: {passed}"
        )

    print()

    print(
        f"Source videos: "
        f"{clip_manifest['video_id'].nunique():,}"
    )

    print(
        f"Total clips: "
        f"{len(clip_manifest):,}"
    )

    print()

    print("Clip counts by split:")

    print(
        clip_manifest["split"]
        .value_counts()
        .to_string()
    )

    print()

    print("Clip counts by binary label:")

    print(
        clip_manifest["binary_label"]
        .value_counts(dropna=False)
        .to_string()
    )

    print()

    print("Clip counts by category:")

    print(
        clip_manifest["category"]
        .value_counts()
        .to_string()
    )

    print()

    print(
        f"CSV saved to: {csv_path}"
    )

    print(
        f"Parquet saved to: {parquet_path}"
    )


if __name__ == "__main__":
    main()