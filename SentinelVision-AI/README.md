# SentinelVision AI

Real-world surveillance video anomaly detection using UCF-Crime videos, leakage-safe clip generation, frozen VideoMAE embeddings, and supervised anomaly-risk classification.

## Final Result

The best model was:

**Frozen VideoMAE embeddings + Logistic Regression**

| Metric | Score |
|---|---:|
| ROC-AUC | 0.9021 |
| PR-AUC | 0.8775 |
| F1 | 0.8283 |

This model outperformed the unsupervised anomaly detection baselines and showed that pretrained video representations can strongly improve clip-level anomaly-risk classification.


## Project Workflow

```text
Raw UCF-Crime videos
→ video inventory
→ video validation
→ leakage-safe train/validation/test split
→ 4-second clip manifest
→ VideoMAE clip embeddings
→ anomaly detection baselines
→ supervised classifier
→ final model comparison
```

## Model Comparison

| Model | ROC-AUC | PR-AUC | F1 |
|---|---:|---:|---:|
| Distance Threshold Baseline | 0.6950 | 0.7743 | 0.6290 |
| Isolation Forest | 0.6659 | 0.7327 | 0.6364 |
| Logistic Regression on VideoMAE Embeddings | 0.9021 | 0.8775 | 0.8283 |


## Tech Stack

- Python
- Pandas / NumPy
- OpenCV
- PyTorch
- Hugging Face Transformers
- VideoMAE
- Scikit-learn
- Matplotlib
- Parquet
- Git / GitHub