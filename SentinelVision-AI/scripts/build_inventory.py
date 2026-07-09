from pathlib import Path

from sentinelvision.data.inventory import (
    build_video_inventory,
)
from sentinelvision.utils.config import load_config


def main() -> None:
    """
    Build and save the UCF-Crime video inventory.
    """
    config = load_config(
        "configs/data.yaml"
    )

    raw_dir = Path(
        config["data"]["raw_dir"]
    )

    metadata_dir = Path(
        config["data"]["metadata_dir"]
    )

    allowed_extensions = config[
        "video"
    ]["allowed_extensions"]

    # Make sure the metadata directory exists.
    metadata_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        f"Scanning videos in: {raw_dir.resolve()}"
    )

    inventory = build_video_inventory(
        raw_dir=raw_dir,
        allowed_extensions=allowed_extensions,
    )

    # Stop clearly when no videos are found.
    if inventory.empty:
        print(
            "No videos found."
        )

        print(
            "Place the UCF-Crime dataset inside data/raw/"
        )

        return

    csv_path = (
        metadata_dir
        / "video_inventory.csv"
    )

    parquet_path = (
        metadata_dir
        / "video_inventory.parquet"
    )

    # CSV is easy to inspect manually.
    inventory.to_csv(
        csv_path,
        index=False,
    )

    # Parquet is faster and better typed for pipelines.
    inventory.to_parquet(
        parquet_path,
        index=False,
    )

    print()
    print("Inventory complete.")
    print(
        f"Videos found: {len(inventory):,}"
    )

    print(
        f"Readable videos: "
        f"{inventory['is_readable'].sum():,}"
    )

    print(
        f"Unreadable videos: "
        f"{(~inventory['is_readable']).sum():,}"
    )

    print(
        f"CSV saved to: {csv_path}"
    )

    print(
        f"Parquet saved to: {parquet_path}"
    )


if __name__ == "__main__":
    main()