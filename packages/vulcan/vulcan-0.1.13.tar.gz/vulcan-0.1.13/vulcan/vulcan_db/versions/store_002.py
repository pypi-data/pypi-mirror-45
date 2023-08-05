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

import os
import re
from datetime import datetime
from textwrap import dedent
from random import choice
from typing import *
from collections import Counter

import arrow

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import select
from sqlalchemy.orm import column_property

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, VARCHAR, TEXT
import sqlalchemy

version = 2

Base = declarative_base()

from vulcan.lib.libtypes import *

class Common(object):
    def as_dict(self):
        obj = {}
        for k,v in self.__dict__.items():
            if k not in ['_sa_instance_state']:
                obj[k] = v if v != "0" else ''
        return obj

class Card(Base, Common):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    question = Column(String, default="")
    answer = Column(String, default="")
    paused = Column(Integer, default=0)
    preamble = Column(String, default="")
    context = Column(String, default="")
    # whether the answer spans multiple lines
    # this is a computed column
    multi = column_property(answer.contains('\n'))

    @typechecked
    def __repr__(self) -> str:
        return dedent("""
            Q: %s
            A: %s
            Successes: %i
            Wrong: %i
            """) % (self.question, self.answer, self.successes, self.failures)

    @property
    @typechecked
    def successes(self) -> int:
        """
        Return the number of times this card was attemped and succeeded.
        """
        return len(list(filter(lambda x: x.success, self.history)))

    @property
    @typechecked
    def tags(self) -> List[int]:
        """
        Returns tags, but as a list of individual tags
        """
        return [x.strip() for x in self.context.split(',')]

    @property
    @typechecked
    def failures(self) -> int:
        """
        Return the number of times this card was attemped and failed.
        """
        return len(list(filter(lambda x: not x.success, self.history)))

    @property
    @typechecked
    def attempts(self) -> int:
        """
        Return the number of times the this card was attempted.
        """
        return len(self.history)

    @property
    @typechecked
    def cloze(self) -> str:
        """
        Return the question's close if it's present.
        """
        try:
            m = re.search(r'{c:([^}]+)}', self.question)
            return m.group(1) if m else ""
        except:
            return ""

    @property
    @typechecked
    def clozed_preamble(self) -> str:
        """
        Perform cloze substitution: if a cloze exists
        in the question, then it's used to automatically
        generate clozes in the preamble field.
        """
        cre = self.cloze
        if cre:
            try:
                clozed_preamble = self.preamble
                search_preamble = clozed_preamble
                matches = re.findall(cre, clozed_preamble)
                if matches:
                    cloze = choice(list(set(matches)))
                    counts = Counter(matches)
                    for cloze in [cloze]*counts[cloze]:
                        f = re.search(cloze, search_preamble)
                        if f:
                            rep = '{c:%s}'%cloze
                            clozed_preamble = clozed_preamble[:f.start()] + rep + clozed_preamble[f.end():]
                            search_preamble = search_preamble[:f.start()] + '_'*len(rep) + search_preamble[f.end():]
                return clozed_preamble
            except:
                return self.preamble
        else:
            return self.preamble

    @property
    @typechecked
    def clozed_question(self) -> str:
        """
        Since questions can contain clozes, remove them to present the question
        cloze-free to the user.
        """
        if self.cloze:
            return re.sub("{c:.*}", '', self.question).strip()
        return self.question.strip()

    @property
    @typechecked
    def lines(self) -> [str]:
        """
        Returns the preamble split into lines.
        """
        return len(self.preamble.split('\n'))

    @typechecked
    def pop(self) -> None:
        """
        Undo history! Remove the last item that was added onto the history.
        Useful when making mistakes.
        """
        if len(self.history):
            self.history = self.history[:-2]

    @typechecked
    def as_dict(self) -> Dict:
        """
        Get card as a json-serializable dict. Useful for exporting. This might
        disappear at some point if the schema gets too complex.
        """
        card_dict = super(Card, self).as_dict()
        card_dict["history"] = [x.as_dict() for x in self.history]
        return card_dict

    @typechecked
    def viewed_today(self) -> bool:
        """
        Return whether the card was viewed today or not
        """
        return any([arrow.get(h.date).date() == datetime.now().date() for h in self.history])

    @property
    @typechecked
    def last_draw_timestamp(self) -> datetime:
        """
        Returns the timestamp of when the card was last viewed.
        """
        if len(self.history):
            return datetime.fromtimestamp(self.history[-1].date)
        else:
            return datetime.fromtimestamp(0)

    @typechecked
    def compare_answer(self, answer: str) -> bool:
        """
        Returns whether the given answer matches with the card's answer.
        If this card is of type python, then it tries to format the code
        before comparing it.
        """
        if self.context == 'python':
            try:
                from yapf.yapflib.yapf_api import FormatCode
                return FormatCode(self.answer)[0].strip() == FormatCode(answer)[0].strip()
            except:
                pass
        return self.answer.lower().strip() == answer.lower().strip()

    @staticmethod
    @typechecked
    def from_dict(d: Dict):
        """
        Creates a new card from the dict provided. Useful for importing cards
        from json.
        """
        del d['multi']
        d['history'] = [History(**h) for h in d['history']]
        return Card(**d)


class History(Base, Common):
    """
    Used to track whether the user responded to the questions right or wrong
    """
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)
    success = Column(Integer)
    qid = Column(Integer, ForeignKey('cards.id'))
    card = relationship("Card", back_populates="history")


Card.history = relationship("History", order_by=History.date, back_populates="card", cascade="save-update, merge, delete")


class MigrateVersion(Base):
    __tablename__ = 'migrate_version'
    repository_id = Column(VARCHAR(250), primary_key=True)
    repository_path = Column(TEXT)
    version = Column(Integer)
