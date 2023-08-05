# -*- coding: utf-8 -*-

# Copyright (C) 2019 github.com/shyal
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


import re
from collections import namedtuple
from functools import reduce

from vulcan.lib.libtypes import *


class FormattedText:

    """
    Formatted text is a list of tuples.
    It can be passed directly to a urwid Text().
    """

    @typechecked
    def __init__(self, items: Union[Fragments, str]) -> None:
        if type(items) is list:
            self.__items = items
        elif type(items) is str:
            self.__items = [('', items)]
        self.__i = 0


    @property
    @typechecked
    def items(self) -> Fragments:
        return self.__items

    @property
    @typechecked
    def width(self) -> int:
        """
        Returns the width, in characters of this FormattedText.
        Make sure seperate_newlines has been called first.
        """
        _m = 0
        m = 0
        for it in self.__items:
            if it[1] == '\n':
                m = max(_m, m)
            _m += len(it[1])
        if m == 0:
            return _m
        return m

    @typechecked
    def __iter__(self) -> 'FormattedText':
        return self

    def __next__(self):
        if self.__i < len(self.__items)-1:
            n = self.__items[self.__i]
            self.__i += 1
            return n
        else:
            raise StopIteration

    @typechecked
    def __eq__(self, other) -> bool:
        return self.__items == other

    @typechecked
    def __getitem__(self, key)  -> Fragment:
        return self.__items[key]

    @typechecked
    def __str__(self) -> str:
        return str(self.__items)

    @typechecked
    def __repr__(self) -> str:
        return str(self.__items)

    @typechecked
    def merge_non_styled_items(self) -> None:
        plain = ''
        j = self.__items
        hl = []
        for it in j:
            if it[0] == '':
                if it[1] == '\n':
                    if plain:
                        hl.append(('', plain))
                        plain = ''
                    hl.append(('', '\n'))
                else:
                    plain += it[1]
            elif plain:
                hl.append(('', plain))
                plain = ''
            if it[0]:
                hl.append(it)
        self.__items = hl

    @typechecked
    def seperate_newlines(self) -> None:
        hl = []
        j = self.__items
        for it in j:
            if '\n' in it[1]:
                hl.append(('', '\n'))
                splits = it[1].split('\n')
                for i in range(len(splits)):
                    hl.append(('', splits[i]))
                    if i < len(splits)-2:
                        hl.append(('', '\n'))
            else:
                hl.append(it)
        self.__items = hl

    @property
    @typechecked
    def plain_text(self) -> str:
        return "".join([x[1] for x in self.__items])

    @typechecked
    def __isolate_position(self, position) -> None:
        start, end = position
        dist = 0
        for i, it in enumerate(self.__items):
            if dist <= start and end <= dist + len(it[1]):
                stripped_cloze = it[1][start-dist:end-dist]
                before = it[1][:start-dist]
                after = it[1][end-dist:]
                assert (len(before) + len(stripped_cloze) + len(after)) == len(it[1])
                self.__items[i] = ('cloze', stripped_cloze)
                if after:
                    self.__items.insert(i+1, (it[0], after))
                if before:
                    self.__items.insert(i, (it[0], before))
            dist += len(it[1])

    @typechecked
    def isolate_positions(self, positions) -> None:
        for p in positions:
            self.__isolate_position(p)

    @typechecked
    def __replace_cloze(self, position, cloze) -> None:
        start, end = position
        dist = 0
        for i, it in enumerate(self.__items):
            if dist <= start and end <= dist + len(it[1]):
                self.__items[i] = ('cloze', cloze)
            dist += len(it[1])

    @typechecked
    def replace_clozes(self, positions: List[Tuple[int, int]], clozes: List[str]) -> None:
        for i, p in enumerate(positions):
            self.__replace_cloze(p, clozes[i])


class ClozedText(str):

    @typechecked
    def __init__(self, content: str) -> None:
        self.__content = content
        self.__cloze_positions = []
        self.__clozes = []

        for m in re.finditer("{c:[^}]+}", self.__content):
            self.__cloze_positions.append((m.start(), m.end()))
            self.__clozes.append(m.group(0))

    @property
    @typechecked
    def positions(self) -> List[Tuple]:
        return self.__cloze_positions

    @property
    @typechecked
    def clozes(self) -> List[str]:
        return self.__clozes

    @property
    @typechecked
    def strip_clozes(self) -> str:
        stripped = self.__content
        for cloze in re.finditer("{c:([^}]+)}", self.__content):
            stripped = stripped.replace(cloze.group(0), "_"*(len(cloze.group(0))))
        return stripped


