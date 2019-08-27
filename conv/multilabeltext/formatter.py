# coding=utf-8
# Copyright 2019 YAM AI Machinery Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
>>> text = 'this is a text'
>>> labels = { '__label__a', '__label__b' }
>>> mlt = MultiLabelText(text)
>>> for lab in labels:
...     mlt.add_label(lab)
>>> mlt.text == text
True
>>> mlt.labels == labels
True
"""


import re
from util.prepro import normalize_label, normalize


class MultiLabelText:
    def __init__(self, text=''):
        self.text = text
        self.labels = set()

    def set_text(self, text):
        self.text = text

    def add_word(self, word):
        self.text += (' ' + word)

    def add_label(self, label):
        self.labels.add(label)


class Formatter:
    def __init__(self, cache_label=True):
        self.cache_label = cache_label
        if cache_label:
            self.cached_labels = {}

    @staticmethod
    def format_label(label):
        return label

    @staticmethod
    def format_text(text):
        return text

    def format(self, mlt):
        for_mlt = MultiLabelText(self.format_text(mlt.text))
        for lab in mlt.labels:
            if self.cache_label:
                can_lab = self.cached_labels.get(lab)
                if not can_lab:
                    can_lab = self.format_label(lab)
                self.cached_labels[lab] = can_lab
            else:
                can_lab = self.format_label(lab)
            for_mlt.add_label(can_lab)
        return for_mlt


class FromFastText(Formatter):
    def __init__(self, cache_label=True):
        super(self.__class__, self).__init__(cache_label)

    @staticmethod
    def format_label(label):
        return re.sub(r'^__label__', '', label)


class ToFastText(Formatter):
    def __init__(self, cache_label=True):
        super(self.__class__, self).__init__(cache_label)

    @staticmethod
    def format_label(label):
        return '__label__' + normalize_label(label)

    @staticmethod
    def format_text(text):
        return normalize(text)


class Normalizer(Formatter):
    def __init__(self, cache_label=True):
        super(self.__class__, self).__init__(cache_label)

    @staticmethod
    def format_label(label):
        return normalize_label(label)

    @staticmethod
    def format_text(text):
        return normalize(text)