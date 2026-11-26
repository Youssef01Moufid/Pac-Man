CONFIG ?= config_file.json
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint lint-strict

install:
	uv sync

run:
	uv run python pac-man.py $(CONFIG)

debug:
	uv run python -m pdb pac-man.py $(CONFIG)

clean:
	find . -path ./.venv -prune -o -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf dist build pac-man.spec

build:
	uv run pyinstaller --onefile --name pac-man \
	  --add-data "assets:assets" \
	  --add-data "config_file.json:."\
	  pac-man.py

lint:
	uv run flake8 .
	uv run mypy . $(MYPY_FLAGS)
