install:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .

.PHONY: install test lint