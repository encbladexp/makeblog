# makeblog

A very simple solution for static Blogs without PHP,MySQL and other dynamic not
required stuff. Mostly inspired by /dev/null

## Requirements

* Python 3
* Jinja 2
* Pygments
* YAML
* PyTZ

## Usage

Create a new Blog:

    ./makeblog -i

Create your first article:

    ./makeblog -t "Your new article"

Build the whole Blog:

    ./makeblog -b

Start the Test Server:

    ./makeblog -s
