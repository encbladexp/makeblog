# makeblog
[![Build Status](https://travis-ci.org/encbladexp/makeblog.svg?branch=master)](https://travis-ci.org/encbladexp/makeblog)
[![Requirements Status](https://requires.io/github/encbladexp/makeblog/requirements.svg?branch=master)](https://requires.io/github/encbladexp/makeblog/requirements/?branch=master)

A very simple solution for static Blogs without PHP,MySQL and other dynamic not
required stuff. Mostly inspired by /dev/null

## Requirements

* Python >= 3.6
* Jinja 2 >= 2.10
* Pygments
* PyTZ

## Setup / Update

    pipenv install

## Usage

Enable the makeblog pipenv in the current shell:

    pipenv shell

Now switch to your blog's root directory or an empty directory for a new blog, and lets the
magic begin…

Create a new Blog:

    makeblogctl -i

Create your first article:

    makeblogctl -t "Your new article"

Build the whole Blog:

    makeblogctl -b

Start the Test Server:

    makeblogctl -s
