test:
	python -m unittest

coverage:
	coverage erase
	coverage run -m unittest
	coverage report
	coverage html
