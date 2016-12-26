.PHONY: test flake8

VENV := $(shell echo $(VIRTUAL_ENV))
FLAKE = $(VENV)/bin/flake8
PYTEST = $(VENV)/bin/pytest

flake8:
	$(FLAKE) longform --statistics

test:
	$(PYTEST) ./longform

pytest_check:
	$(PYTEST) ./longform --collectonly
