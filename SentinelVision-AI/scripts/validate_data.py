from pathlib import Path

import pandas as pd

from sentinelvision.data.validator import validate_inventory
from sentinelvision.utils.config import load_config


def main() -> None:
    """
    Validate the generated video inventory.
    """
    config = load_config(
        "configs/data.yaml"
    )

    metadata_dir = Path(
        config["data"]["metadata_dir"]
    )

    minimum_duration = config[
        "validation"
    ]["minimum_duration_seconds"]

    inventory_path = (
        metadata_dir
        / "video_inventory.parquet"
    )

    if not inventory_path.exists():
        raise FileNotFoundError(
            "Video inventory not found. "
            "Run python scripts/build_inventory.py first."
        )

    inventory = pd.read_parquet(
        inventory_path
    )

    valid_videos, invalid_videos = validate_inventory(
        inventory=inventory,
        minimum_duration_seconds=minimum_duration,
    )

    valid_path = (
        metadata_dir
        / "valid_videos.parquet"
    )

    invalid_path = (
        metadata_dir
        / "invalid_videos.parquet"
    )

    valid_videos.to_parquet(
        valid_path,
        index=False,
    )

    invalid_videos.to_parquet(
        invalid_path,
        index=False,
    )

    print("Validation complete.")
    print(
        f"Total videos: {len(inventory):,}"
    )
    print(
        f"Valid videos: {len(valid_videos):,}"
    )
    print(
        f"Invalid videos: {len(invalid_videos):,}"
    )

    if not invalid_videos.empty:
        print()
        print("Invalid video reasons require review.")
        print(
            invalid_videos[
                [
                    "file_name",
                    "category",
                    "is_readable",
                    "fps",
                    "frame_count",
                    "duration_seconds",
                ]
            ]
            .head(20)
            .to_string(index=False)
        )


if __name__ == "__main__":
    main()