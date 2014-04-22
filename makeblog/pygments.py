# makeblog - A simple offline Blog.
# Copyright (C) 2013-2014 Stefan J. Betz <info@stefan-betz.net>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from re import compile, escape, DOTALL
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from pygments import highlight
from makeblog.tools import directorymaker

code_re = compile(
    r"(?:^|\s)"
    r"\$\$code"
    r"(?P<args>\([^\r\n]*\))?"
    r"[^\r\n]*\r?\n"
    r"(?P<code>.*?)\s\$\$/code", DOTALL)


def pygments_css(formatter):
    with open(directorymaker('css/pygments_fruity.css'), "w") as f:
        f.write(formatter.get_style_defs('.pygments_fruity'))


def highlight_code(code, language, formatter):
    try:
        lexer = get_lexer_by_name(language)
    except ClassNotFound:
        lexer = get_lexer_by_name("text")
    highlighted = "\n\n{0}\n\n".format(highlight(code, lexer, formatter))
    return highlighted


def pygmentify(func):
    def decorator(self):
        post = func(self)
        substitutions = {}
        for match in code_re.finditer(post):
            args = match.group('args')
            lang = 'text'
            if args:
                if 'lang' in args:
                    lang = args.strip('(').strip(')').split('=')[1]
            formatter = HtmlFormatter(cssclass='pygments_fruity',
                                      style='fruity')
            pygments_css(formatter)
            substitutions[match.group()] = highlight_code(match.group('code'),
                                                          lang, formatter)
        if len(substitutions) > 0:
            p = compile('|'.join(map(escape, substitutions)))
            post = p.sub(lambda x: substitutions[x.group(0)], post)
            return post
        else:
            return post
    return decorator
