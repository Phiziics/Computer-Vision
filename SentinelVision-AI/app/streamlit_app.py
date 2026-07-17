from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="SentinelVision AI",
    page_icon="🎥",
    layout="wide"
)

st.title("SentinelVision AI")
st.subheader("Surveillance Video Anomaly Detection")

st.markdown(
    """
    SentinelVision AI scores surveillance video clips for anomaly risk.

    Final model:

    **Frozen VideoMAE embeddings + Logistic Regression**

    | Metric | Score |
    |---|---:|
    | ROC-AUC | 0.9021 |
    | PR-AUC | 0.8775 |
    | F1 | 0.8283 |
    """
)

metrics_path = Path("artifacts/metrics/supervised_videomae_results.csv")

if metrics_path.exists():
    results = pd.read_csv(metrics_path)

    st.markdown("## Final Model Results")
    st.dataframe(results)
else:
    st.warning(
        "Could not find artifacts/metrics/supervised_videomae_results.csv"
    )

st.markdown("## Project Workflow")

st.code(
    """
Raw UCF-Crime videos
→ video inventory
→ validation
→ leakage-safe split
→ 4-second clips
→ frozen VideoMAE embeddings
→ Logistic Regression classifier
→ anomaly-risk score
    """,
    language="text",
)
st.markdown("## Business Value")

st.markdown(
    """
    This project helps security teams prioritize high-risk footage for review.

    It is designed as decision support, not a replacement for human reviewers.
    """
)