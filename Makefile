PYTHON=/usr/bin/env python3
PYLINT=/usr/bin/env pylint3

lint:
	${PYLINT} --rcfile magic/.pylintrc magic && flake8 magic && black --check --line-length 79 magic && \
	${PYLINT} --rcfile tests/.pylintrc tests && flake8 tests && black --check --line-length 79 tests

format:
	black --line-length 79 magic && \
	black --line-length 79 tests

test:
	${PYTHON} -m pytest -x -l
