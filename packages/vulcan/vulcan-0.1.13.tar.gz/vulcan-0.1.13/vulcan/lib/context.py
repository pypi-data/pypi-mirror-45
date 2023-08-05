# -*- coding: utf-8 -*-

# Copyright (C) 2017 github.com/shyal
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import getpass
from collections import defaultdict

import vulcan.lib.highlighter as hi
from vulcan.lib.store import Card
from vulcan.lib.text_utils import *

from urwid import *
from textwrap import dedent

class LineWidget(Columns):

    """
    Individual lines of code in vulcan's main view.
    Reprensenting the code as individual lines enables us to
    treat each line as a column. This is so we can substitute
    clozes with urwid Edit widgets.
    """

    def __init__(self, items, __edit_change_manager, cloze_to_edit=False):
        self.items = items
        self.__ignore_callback = False
        self.__edit_change_manager = __edit_change_manager
        columns = []
        text = []
        for it in items:
            if it[0] == 'cloze':
                if text:
                    columns.append(('pack', Text(text)))
                    text = []
                cloze = re.search("{c:([^}]+)}", it[1]).group(1)
                edit = self.__edit_change_manager.Edit(cloze)
                columns.append(('fixed', len(cloze), edit))
            else:
                text.append(it)

        if text:
            columns.append(Text(text))

        self.__super.__init__(columns)

    def __str__(self):
        return str(self.items)

    def __repr__(self):
        return str(self.items)

class EditChangeHandler:

    """
    Manage Clozes / urwid Edits. The same clozes may end up appearing
    multiple times at once, in which case they'll all update simultaneously.

    Likewise we can check whether they were all entered correctly etc.
    """

    def __init__(self):
        self.__edit = defaultdict(list)
        self.__text_change = ""

    def Edit(self, cloze):
        edit = Edit('', len(cloze) * '_')
        self.__edit[cloze].append(edit)
        connect_signal(edit, 'change', self.change, cloze)
        connect_signal(edit, 'postchange', self.postchange, cloze)
        return edit

    def change(self, edit, text, cloze):
        self.__text_change = text

    def postchange(self, edit, text, cloze):
        for edit in self.__edit[cloze]:
            text = edit._normalize_to_caption(self.__text_change)
            edit.highlight = None
            edit._edit_text = text[:len(cloze)]
            if edit.edit_pos > len(cloze):
                edit.edit_pos = len(cloze)
            edit._invalidate()

    @property
    def has_clozes(self):
        for k, v in self.__edit.items():
            for e in v:
                return True
        return False

    @property
    def clozes_are_correct(self):
        correct = True
        for k, v in self.__edit.items():
            for e in v:
                correct = correct and e.edit_text == k
                has_closes = True
        return correct

class CardContext(WidgetWrap):

    """
    Cards can have different looks based on which language they're in.
    By default, they just show up in a bash-esque environment, however
    they can appear in an interactive python shell, a mysql shell etc. 
    """

    def __init__(self, card, command, banner, prompt):
        self.card = card
        self.__command = command
        self.__banner = banner
        self.__prompt = prompt
        self.__edit_change_manager = EditChangeHandler()

        ct = ClozedText(card.clozed_preamble)
        highlighted = hi.highlight(ct.strip_clozes)
        positions = ct.positions
        highlighted.isolate_positions(positions)
        highlighted.replace_clozes(positions, ct.clozes)

        lines = self.lines(highlighted)
        pile = []
        if self.__banner:
            pile.append(Text(('gray', self.__banner)))
        formatted_prompt = FormattedText(self.__prompt)
        if lines:
            cols = [
                ('fixed', formatted_prompt.width, Pile([Text(formatted_prompt.items)]*len(lines)))
            ]
            cols.append(('weight', 1, Pile(lines)))

            pile.append(Columns(cols))

        if self.card.clozed_question:
            pile.append(Text(formatted_prompt.items + [('dark blue', "# "), ('dark blue', self.card.clozed_question)]))

        if command:
            pile.insert(0, Text(bash_prompt() + [command]))

        self.__super.__init__(Pile(pile))

    @property
    def clozes_are_correct(self):
        return self.__edit_change_manager.clozes_are_correct

    @property
    def has_clozes(self):
        return self.__edit_change_manager.has_clozes

    def lines(self, pygt):
        lines = []
        line = []
        for it in pygt:
            if it[1] == '\n':
                if line:
                    lines.append(LineWidget(line, self.__edit_change_manager))
                else:
                    lines.append(Text(''))
                line = []
            else:
                line.append(it)
        if line:
            lines.append(LineWidget(line, self.__edit_change_manager))
        return lines

    @property
    def prompt(self):
        if isinstance(self.__prompt, str):
            return [self.__prompt]
        elif isinstance(self.__prompt, list):
            return self.__prompt

    @property
    def command(self):
        if isinstance(self.__command, str):
            if self.__command:
                return [self.__command]
            return []
        elif isinstance(self.__command, list):
            return self.__command

class PythonCardContext(CardContext):

    def __init__(self, *args, **kwargs):
        command = "python"
        banner = """Python 2.7.10 (default, Jul 14 2015, 19:46:27)
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.39)] on darwin
Type "help", "copyright", "credits" or "license" for more information."""
        prompt = ">>> "
        super(PythonCardContext, self).__init__(command=command, banner=banner, prompt=prompt, *args, **kwargs)

class SQLite3CardContext(CardContext):

    def __init__(self, *args, **kwargs):
        command = "sqlite3"
        banner = """SQLite version 3.8.7.4 2014-12-09 01:34:36
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database."""
        prompt = "sqlite> "
        super(SQLite3CardContext, self).__init__(command=command, banner=banner, prompt=prompt, *args, **kwargs)

class NodeCardContext(CardContext):

    def __init__(self, *args, **kwargs):
        command = "node"
        prompt = "> "
        super(NodeCardContext, self).__init__(command=command, banner='', prompt=prompt, *args, **kwargs)

class RubyCardContext(CardContext):

    def __init__(self, *args, **kwargs):
        command = "ruby"
        banner = """ruby 2.0.0p481 (2014-05-08 revision 45883) [universal.x86_64-darwin14]"""
        prompt = ""
        super(RubyCardContext, self).__init__(command=command, banner=banner, prompt=prompt, *args, **kwargs)

class SQLCardContext(CardContext):

    def __init__(self, *args, **kwargs):
        command = "mysql"
        banner = """Welcome to the MariaDB monitor.  Commands end with ; or \\g.
Your MariaDB connection id is 5
Server version: 10.1.23-MariaDB Homebrew

Copyright (c) 2000, 2017, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\\h' for help. Type '\\c' to clear the current input statement."""
        prompt = "MariaDB [(none)]> "
        super(SQLCardContext, self).__init__(command=command, banner=banner, prompt=prompt, *args, **kwargs)

def bash_prompt():
    return [("dark blue", getpass.getuser()), ('', "@"), ("dark green", "vulcan"), ('', ":"),("dark blue", "~ ")]

class BashCardContext(CardContext):

    def __init__(self, *args, **kwargs):
        super(BashCardContext, self).__init__(command='', banner='', prompt=bash_prompt(), *args, **kwargs)

def prompt(card):
    if "python" in card.context:
        return PythonCardContext(card)
    if card.context == "sqlite3":
        return SQLite3CardContext(card)
    if card.context in ['node', 'nodejs', 'react', 'redux']:
        return NodeCardContext(card)
    elif card.context == "sql":
        return SQLCardContext(card)
    elif card.context == "ruby":
        return RubyCardContext(card)
    return BashCardContext(card)

class CardWidget(WidgetWrap):

    def __init__(self, card: Card):
        self.__card = card
        pygt = hi.highlight(card.clozed_preamble)
        lines = self.lines(pygt)

        pile = Columns([
            ('pack', Text('>>> \n'*self.__card.lines)),
            ('weight', 1, Pile(lines))
        ])
        self.__super.__init__(pile)

    def lines(self, pygt):
        lines = []
        line = []
        for it in pygt:
            if it[1] == '\n':
                if line:
                    lines.append(LineWidget(line))
                else:
                    lines.append(Text(''))
                line = []
            else:
                line.append(it)
        return lines

