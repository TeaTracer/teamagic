lint:
	pylint --rcfile magic/.pylintrc magic && flake8 magic && black --check --line-length 79 magic && \
	pylint --rcfile tests/.pylintrc tests && flake8 tests && black --check --line-length 79 tests

format:
	black --line-length 79 magic && \
	black --line-length 79 tests

test:
	python -m pytest -x -l
