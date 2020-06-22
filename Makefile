mutants:
	mutmut run \
		--paths-to-mutate geci_distance

.PHONY: clean install mutants tests

install:
	pip install --editable .

format:
	black --check geci_distance
	black --check tests

tests: install
	pytest --verbose

clean:
	rm --recursive --force test/__pycache__
	rm --recursive --force geci_distance/__pycache__
	rm --recursive --force geci_distance.egg-info
	rm --force .mutmut-cache
