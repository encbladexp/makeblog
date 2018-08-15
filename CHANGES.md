Changes
=======

Release 0.0.7
-------------
* Removed tools/yaml2json-upgrade.py
* Switched from requirements.txt to Pipfile
* Dropped support for Python <=3.4
* Add support for Python 3.7
* Updated requirements

Release 0.0.6
-------------
* Explicite pinned all requirements
* Support for Python 3.5 and 3.6
* Moved makeblog-bin to makeblogctl
* Replaces multiple occasions of a dash with a single dash in slugify()
* bumpversion Integration

Release 0.0.5
-------------
* Fixed Atom feeds
* Fixed Server mode issues
* Removed support for pypy3 for now (several issues)
* Travis Integration
* Post metadata (author, date, …) has now always the same order
* Moved to python str.format()
* XHTML => HTML5
* More Unittests
* Most stuff are now plugins
* Flattr Support
* Updated requirements

Release 0.0.4
-------------
* First release with github (git) instead of bitbucket (hg)
* Some more Unittests
* Development requirements have now its own requirements.txt file

Release 0.0.3
-------------
* Fixed Ctrl-C in server mode
* Use SO_REUSEADDR for server mode, to avoid socket collisions

Release 0.0.2
-------------
* slugify() now supports filenames with colons
* Load user specified slug from article headers, if specified
* Some Unittests
* Support for multiple authors
* Support for draft rendering
* Support for updating dates on existing/published articles

Release 0.0.1
-------------
* Initial Release
