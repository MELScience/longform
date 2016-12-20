.PHONY: test flake8

VENV := $(shell echo $(VIRTUAL_ENV))
FLAKE = $(VENV)/bin/flake8

flake8:
	$(FLAKE) longform --statistics

test: flake8
