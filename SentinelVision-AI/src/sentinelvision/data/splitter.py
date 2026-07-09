from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


def validate_split_sizes(
    train_size: float,
    validation_size: float,
    test_size: float,
) -> None:
    """
    Confirm that split proportions sum to 1.0.
    """
    total = train_size + validation_size + test_size

    if not abs(total - 1.0) < 1e-8:
        raise ValueError(
            "Train, validation, and test sizes must sum to 1.0. "
            f"Received total: {total}"
        )


def create_video_splits(
    inventory: pd.DataFrame,
    train_size: float = 0.70,
    validation_size: float = 0.15,
    test_size: float = 0.15,
    stratify_column: str = "category",
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Create leakage-safe train, validation, and test splits
    at the source-video level.

    Each video receives exactly one split assignment.
    """
    validate_split_sizes(
        train_size=train_size,
        validation_size=validation_size,
        test_size=test_size,
    )

    required_columns = {
        "video_id",
        stratify_column,
    }

    missing_columns = required_columns.difference(
        inventory.columns
    )

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    split_data = inventory.copy()

    # Protect against duplicate source videos.
    if split_data["video_id"].duplicated().any():
        duplicates = split_data.loc[
            split_data["video_id"].duplicated(keep=False),
            "video_id",
        ].unique()

        raise ValueError(
            "Duplicate video_id values found. "
            f"Examples: {duplicates[:10].tolist()}"
        )

    # First split:
    # train vs temporary validation+test pool.
    temporary_size = validation_size + test_size

    train_data, temporary_data = train_test_split(
        split_data,
        test_size=temporary_size,
        stratify=split_data[stratify_column],
        random_state=random_state,
    )

    # Convert validation proportion relative to the
    # temporary pool.
    relative_test_size = (
        test_size / temporary_size
    )

    # Second split:
    # temporary pool -> validation and test.
    validation_data, test_data = train_test_split(
        temporary_data,
        test_size=relative_test_size,
        stratify=temporary_data[stratify_column],
        random_state=random_state,
    )

    train_data = train_data.copy()
    validation_data = validation_data.copy()
    test_data = test_data.copy()

    train_data["split"] = "train"
    validation_data["split"] = "validation"
    test_data["split"] = "test"

    # Recombine into one frozen split manifest.
    split_manifest = pd.concat(
        [
            train_data,
            validation_data,
            test_data,
        ],
        ignore_index=True,
    )

    # Stable ordering makes files easier to compare.
    split_manifest = split_manifest.sort_values(
        by=["split", stratify_column, "video_id"]
    ).reset_index(drop=True)

    return split_manifest


def validate_split_integrity(
    split_manifest: pd.DataFrame,
) -> dict[str, bool]:
    """
    Validate that source videos do not leak
    across train, validation, and test.
    """
    required_columns = {
        "video_id",
        "split",
    }

    missing_columns = required_columns.difference(
        split_manifest.columns
    )

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    valid_split_names = {
        "train",
        "validation",
        "test",
    }

    actual_split_names = set(
        split_manifest["split"].unique()
    )

    valid_names = (
        actual_split_names == valid_split_names
    )

    # Each video should appear exactly once.
    unique_video_assignment = (
        split_manifest.groupby("video_id")["split"]
        .nunique()
        .max()
        == 1
    )

    no_duplicate_video_ids = (
        not split_manifest["video_id"]
        .duplicated()
        .any()
    )

    return {
        "valid_split_names": valid_names,
        "unique_video_assignment": unique_video_assignment,
        "no_duplicate_video_ids": no_duplicate_video_ids,
    }


def save_split_manifest(
    split_manifest: pd.DataFrame,
    output_dir: str | Path,
) -> tuple[Path, Path]:
    """
    Save split assignments as CSV and Parquet.
    """
    output_path = Path(output_dir)

    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_path = output_path / "video_splits.csv"
    parquet_path = output_path / "video_splits.parquet"

    split_manifest.to_csv(
        csv_path,
        index=False,
    )

    split_manifest.to_parquet(
        parquet_path,
        index=False,
    )

    return csv_path, parquet_path