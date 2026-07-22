# Data

This project uses the UCF-Crime real-world surveillance video dataset.

Raw video files are not included in this repository because they are large and should be downloaded from the original dataset source.

The repository contains code, notebooks, project structure, model results, and documentation for reproducing the workflow.

## Data Handling

The pipeline expects raw videos to be stored locally under:

`data/raw/`

That folder is intentionally ignored by Git.

## Pipeline Outputs

The project generates:

- video inventory files
- video validation outputs
- train/validation/test split metadata
- 4-second clip manifest
- VideoMAE embeddings
- model metrics