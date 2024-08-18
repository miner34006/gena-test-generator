PROJECT_NAME=test_generator

.PHONY: install
install:
	pip3 install --quiet --upgrade pip
	pip3 install --quiet -r requirements.txt -r requirements-dev.txt

.PHONY: check-types
check-types:
	python3 -m mypy ${PROJECT_NAME} --implicit-optional --implicit-reexport

.PHONY: check-imports
check-imports:
	python3 -m isort ${PROJECT_NAME} --check-only

.PHONY: sort-imports
sort-imports:
	python3 -m isort ${PROJECT_NAME}

.PHONY: check-style
check-style:
	python3 -m flake8 ${PROJECT_NAME}

.PHONY: lint
lint: check-types check-style check-imports

