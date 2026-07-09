from pathlib import Path

import pandas as pd

from sentinelvision.data.splitter import (
    create_video_splits,
    save_split_manifest,
    validate_split_integrity,
)
from sentinelvision.utils.config import load_config


def main() -> None:
    """
    Create reproducible, leakage-safe
    train/validation/test video splits.
    """
    config = load_config(
        "configs/data.yaml"
    )

    metadata_dir = Path(
        config["data"]["metadata_dir"]
    )

    valid_videos_path = (
        metadata_dir / "valid_videos.parquet"
    )

    if not valid_videos_path.exists():
        raise FileNotFoundError(
            "Valid video inventory not found. "
            "Run python scripts/validate_data.py first."
        )

    valid_videos = pd.read_parquet(
        valid_videos_path
    )

    split_config = config["splits"]

    split_manifest = create_video_splits(
        inventory=valid_videos,
        train_size=split_config["train_size"],
        validation_size=split_config["validation_size"],
        test_size=split_config["test_size"],
        stratify_column=split_config["stratify_column"],
        random_state=split_config["random_state"],
    )

    integrity_results = validate_split_integrity(
        split_manifest
    )

    # Stop immediately if leakage checks fail.
    if not all(integrity_results.values()):
        raise RuntimeError(
            f"Split integrity failed: {integrity_results}"
        )

    csv_path, parquet_path = save_split_manifest(
        split_manifest=split_manifest,
        output_dir=metadata_dir,
    )

    print("Video split creation complete.")
    print()

    print("Integrity checks:")
    for check_name, passed in integrity_results.items():
        print(
            f"  {check_name}: {passed}"
        )

    print()
    print("Split counts:")
    print(
        split_manifest["split"]
        .value_counts()
        .to_string()
    )

    print()
    print("Split proportions:")
    print(
        split_manifest["split"]
        .value_counts(normalize=True)
        .round(4)
        .to_string()
    )

    print()
    print("Category distribution by split:")
    print(
        pd.crosstab(
            split_manifest["category"],
            split_manifest["split"],
        ).to_string()
    )

    print()
    print(f"CSV saved to: {csv_path}")
    print(f"Parquet saved to: {parquet_path}")


if __name__ == "__main__":
    main()