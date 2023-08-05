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

import sys
from collections import OrderedDict

from vulcan.lib.api import FlashcardAlgorithm
from vulcan.lib.store import Cards, Card
from vulcan.lib.prefs import prefs, reset_prefs
from vulcan.lib.store import get_session

class PrefsTags:

    def get(self, key):
        return prefs.get(f"tag_{key}", True)

    def get_all(self):
        tags = {}
        for t in Cards.tags():
            tags[t] = prefs.get(f"tag_{t}", True)
        return tags

    def get_current(self):
        return [k for k, v in self.get_all().items() if v]

    def set(self, key, value):
        prefs["tag_"+key] = value

class VulcanModel(object):

    def __init__(self, db_path):
        self.session = get_session(db_path)
        self.__current_card = None
        self.tags = PrefsTags()
        self.init_algo()

    def init_algo(self):
        self.algo = FlashcardAlgorithm(wdist_weight=1, tdist_weight=0, includeMuli=True, includePaused=False, tags=self.tags.get_current())
        self.algo.init()

    def draw_card(self):
        self.__current_card = self.algo.draw_card()
        return self.__current_card

    @property
    def current_card(self):
        return self.__current_card

    def refresh_tags(self):
        pass

    @current_card.setter
    def current_card(self, value):
        self.__current_card = value

    def remove_card(self, card):
        if card == self.__current_card:
            self.current_card = None
        self.session.delete(card)
        self.session.commit()
        # TODO: this is horrible... please clean up
        self.init_algo()

    def add_card(self, question, answer, context, preamble):
        card = Card(question=question, answer=answer, context=context, paused=False, preamble=preamble)
        self.session.add(card)
        self.session.commit()
        # TODO: this is horrible... please clean up
        self.init_algo()

    def pause_card(self, card):
        card.paused = True
        self.session.commit()

    def drop(self):
        Cards.drop()
