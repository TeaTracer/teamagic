lint:
	pylint3 magic && flake8 magic && black --check --line-length 79 magic

format:
	black --line-length 79 magic

test:
	python3 -m pytest -x
