# makeblog [![Build Status](https://travis-ci.org/encbladexp/makeblog.svg?branch=master)](https://travis-ci.org/encbladexp/makeblog)


A very simple solution for static Blogs without PHP,MySQL and other dynamic not
required stuff. Mostly inspired by /dev/null

## Requirements

* Python >= 3.3
* Jinja 2 >= 2.7
* Pygments
* PyTZ

## Setup

    pip install -r requirements/production.txt
    python setup.py install

## Usage

Create a new Blog:

    makeblogctl -i

Create your first article:

    makeblogctl -t "Your new article"

Build the whole Blog:

    makeblogctl -b

Start the Test Server:

    makeblogctl -s
