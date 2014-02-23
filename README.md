# makeblog

A very simple solution for static Blogs without PHP,MySQL and other dynamic not
required stuff. Mostly inspired by /dev/null

## Requirements

* Python >= 3.3
* Jinja 2 >= 2.7
* Pygments
* PyTZ

## Setup

    pip install -r requirements.txt
    python setup.py install

## Usage

Create a new Blog:

    makeblog-bin -i

Create your first article:

    makeblog-bin -t "Your new article"

Build the whole Blog:

    makeblog-bin -b

Start the Test Server:

    makeblog-bin -s
