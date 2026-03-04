install:
	pip install poetry
	poetry install

run:
	poetry run python3 a_maze_ing.py config.txt

debug:
	poetry run python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache *.pyc dist
	rm -rf mazegen/__pycache__ mazegen/*.egg-info
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	find . -name "poetry.lock" -delete

lint:
	poetry run flake8 . --exclude=.venv,__pycache__
	poetry run mypy mazegen/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

build:
	poetry build
	cp dist/*.whl .
	cp dist/*.tar.gz .
	rm -rf dist