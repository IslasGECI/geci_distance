mutation:
	mutmut run \
		--paths-to-mutate geci_distance

.PHONY: clean install mutation tests

install:
	pip install --editable .

tests: install
	pytest --verbose

clean:
	rm --recursive --force test/__pycache__
	rm --recursive --force geci_distance/__pycache__
	rm --recursive --force geci_distance.egg-info
	rm --force .mutmut-cache