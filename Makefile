test:
	python -m unittest

coverage:
	coverage erase
	coverage run -m unittest
	coverage report
	coverage html

clean:
	-rm -r htmlcov
	-rm -r dst
	-rm -r build
