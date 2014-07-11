test:
	python -m unittest

coverage:
	coverage erase
	coverage run -m unittest
	coverage report --include="makeblog*"
	coverage html --include="makeblog*"

clean:
	-rm -r htmlcov
	-rm -r dst
	-rm -r build
