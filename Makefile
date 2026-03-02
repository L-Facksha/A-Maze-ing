install:
	poetry install

run:
	poetry run python3 a_maze_ing.py config.txt

debug:
	poetry run python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache *.pyc
	rm -rf mazegen/__pycache__ mazegen/dist mazegen/*.egg-info
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

lint:
	poetry run flake8 .
	poetry run mypy a_maze_ing.py config.py display.py m_to_hex.py --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	poetry run flake8 .
	poetry run mypy a_maze_ing.py config.py display.py m_to_hex.py --strict

build:
	cd mazegen && python3 -m build
	cp mazegen/dist/mazegen-*.whl .
	cp mazegen/dist/mazegen-*.tar.gz .
