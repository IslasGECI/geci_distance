mutants:
	mutmut run --paths-to-mutate geci_distance

.PHONY: clean install lint mutants tests

install:
	pip install --editable .

format:
	black --check --line-length 100 geci_distance
	black --check --line-length 100 tests

lint:
	flake8 --max-line-length 100 geci_distance
	flake8 --max-line-length 100 tests
	pylint geci_distance
	pylint tests

tests: install
	pytest --cov=geci_distance --cov-report=xml --verbose && \
	codecov --token=18f4c788-e1a1-442b-8e15-bd0e10fa8ff1

clean:
	rm --force .mutmut-cache
	rm --recursive --force geci_distance.egg-info
	rm --recursive --force geci_distance/__pycache__
	rm --recursive --force test/__pycache__
