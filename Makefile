venv = ~/.venvs/makeblog

test:
	$(venv)/bin/python -m unittest

coverage:
	$(venv)/bin/coverage erase
	$(venv)/bin/coverage run -m unittest
	$(venv)/bin/coverage report --include="makeblog*" --omit="makeblog/test_*"
	$(venv)/bin/coverage html --include="makeblog*" --omit="makeblog/test_*"

clean:
	-rm -r htmlcov
	-rm -r dst
	-rm -r build

virtualenv:
	mkdir -p $(venv)
	virtualenv $(venv)
	$(venv)/bin/pip install -r requirements_dev.txt
	$(venv)/bin/python setup.py install
