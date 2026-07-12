PYTHON ?= python

.PHONY: validate test package

validate:
	$(PYTHON) scripts/validate_contracts.py

test:
	$(PYTHON) -m unittest discover -s tests -v

package:
	$(PYTHON) scripts/package_release.py
