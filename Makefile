test:
	python -m unittest

coverage:
	coverage erase
	coverage run -m unittest
	coverage report --include="makeblog*" --omit="makeblog/test_*"
	coverage html --include="makeblog*" --omit="makeblog/test_*"

clean:
	-rm -r htmlcov
	-rm -r dst
	-rm -r build
