PROJECT_NAME=test_generator
SCRIPT_FILE=generate_scenarios.py

.PHONY: install
install:
	pip3 install --quiet --upgrade pip
	pip3 install --quiet -r requirements.txt -r requirements-dev.txt

.PHONY: check-types
check-types:
	python3 -m mypy ${PROJECT_NAME} ${SCRIPT_FILE} --implicit-optional --implicit-reexport

.PHONY: check-imports
check-imports:
	python3 -m isort ${PROJECT_NAME} ${SCRIPT_FILE} --check-only

.PHONY: sort-imports
sort-imports:
	python3 -m isort ${PROJECT_NAME} ${SCRIPT_FILE}

.PHONY: check-style
check-style:
	python3 -m flake8 ${PROJECT_NAME} ${SCRIPT_FILE}

.PHONY: lint
lint: check-types check-style check-imports

