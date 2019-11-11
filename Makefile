PYTHON=/usr/bin/env python3
PYLINT=/usr/bin/env pylint3

lint:
	${PYLINT} --rcfile teamagic/.pylintrc teamagic && flake8 teamagic && black --check --line-length 79 teamagic
	${PYLINT} --rcfile tests/.pylintrc tests && flake8 tests && black --check --line-length 79 tests

format:
	black --line-length 79 teamagic
	black --line-length 79 tests

test:
	${PYTHON} -m pytest -x -l

install:
	${PYTHON} setup.py install

devinstall: checkinstall venv
	. .venv/bin/activate
	.venv/bin/python3 setup.py install

venv:
	${PYTHON} -m venv .venv

checkinstall:
	${PYTHON} setup.py check -m -s

python: venv
	. .venv/bin/activate
	.venv/bin/python3
