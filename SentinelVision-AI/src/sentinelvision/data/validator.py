import pandas as pd


def validate_inventory(
    inventory: pd.DataFrame,
    minimum_duration_seconds: float = 1.0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split the inventory into valid and invalid video records.
    """
    validated = inventory.copy()

    # A video is valid only if all core conditions pass.
    validated["valid_video"] = (
        validated["is_readable"]
        & validated["fps"].gt(0)
        & validated["frame_count"].gt(0)
        & validated["width"].gt(0)
        & validated["height"].gt(0)
        & validated["duration_seconds"].ge(
            minimum_duration_seconds
        )
        & validated["category"].ne("Unknown")
    )

    valid_videos = validated[
        validated["valid_video"]
    ].copy()

    invalid_videos = validated[
        ~validated["valid_video"]
    ].copy()

    return valid_videos, invalid_videos