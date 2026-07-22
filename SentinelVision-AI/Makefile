.PHONY: help install app docker-build docker-run inventory validate splits clips clean

help:
	@echo "Available commands:"
	@echo "  make install       Install Python dependencies"
	@echo "  make app           Run Streamlit demo app"
	@echo "  make docker-build  Build Docker image"
	@echo "  make docker-run    Run Docker container"
	@echo "  make inventory     Build video inventory"
	@echo "  make validate      Validate raw videos"
	@echo "  make splits        Create leakage-safe splits"
	@echo "  make clips         Create clip manifest"
	@echo "  make clean         Remove Python cache files"

install:
	pip install -r requirements.txt

app:
	streamlit run app/streamlit_app.py

docker-build:
	docker build -t sentinelvision-ai .

docker-run:
	docker run -p 8501:8501 sentinelvision-ai

inventory:
	python scripts/build_inventory.py

validate:
	python scripts/validate_data.py

splits:
	python scripts/create_splits.py

clips:
	python scripts/extract_clips.py

clean:
	python -c "import pathlib, shutil; [shutil.rmtree(path) for path in pathlib.Path('.').rglob('__pycache__')]"