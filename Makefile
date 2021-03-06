all: mutants

.PHONY: all clean check coverage format install lint mutants tests

repo = geci_distance

clean:
	rm --force .mutmut-cache
	rm --recursive --force ${repo}.egg-info
	rm --recursive --force ${repo}/__pycache__
	rm --recursive --force tests/__pycache__
	rm --recursive --force .pytest_cache
	rm --force .coverage
	rm --force coverage.xml

check:
	black --check --line-length 100 ${repo}
	black --check --line-length 100 tests
	flake8 --max-line-length 100 ${repo}
	flake8 --max-line-length 100 tests

coverage: install
	pytest --cov=${repo} --cov-report=xml --verbose && \
	codecov --token=18f4c788-e1a1-442b-8e15-bd0e10fa8ff1

format:
	black --line-length 100 ${repo}
	black --line-length 100 tests

install:
	pip install --editable .

lint:
	flake8 --max-line-length 100 ${repo}
	flake8 --max-line-length 100 tests
	pylint ${repo}
	pylint tests

mutants:
	mutmut run --paths-to-mutate ${repo}

tests: install
	pytest --verbose
