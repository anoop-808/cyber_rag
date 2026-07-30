.PHONY: install run test lint format clean

install:
	pip install -r requirements.txt

run:
	python -m uvicorn app.main:app --reload

test:
	python -m pytest -v

format:
	python -m black app tests

lint:
	python -m ruff check app tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
