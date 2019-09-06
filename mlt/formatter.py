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
>>> labels = { 'Hello,  World.', 'What a  *Wonderful* World!' }
>>> ft_labels_1 = { '__label__' + label for label in labels }
>>> norm_labels = { 'hello_world', 'what_a_wonderful_world' }
>>> ft_labels_2 = { '__label__' + label for label in norm_labels }
>>> mlt = MultiLabelText(text)
>>> for lab in ft_labels_1:
...     mlt.add_label(lab)
>>> mlt.text == text
True
>>> mlt.labels == ft_labels_1
True
>>> fft = FromFastText(cache_labels=True)
>>> norm_mlt = fft.format(mlt)
>>> norm_mlt.text == text
True
>>> norm_mlt.labels == labels
True
>>> tft = ToFastText(normalize_labels=True, word_seq=True, cache_labels=True)
>>> to_mlt = tft.format(norm_mlt)
>>> to_mlt.text == text
True
>>> to_mlt.labels == ft_labels_2
True
>>>
>>> nft = Normalizer(normalize_labels=True, word_seq=True, cache_labels=False)
>>> n_mlt = nft.format(norm_mlt)
>>> n_mlt.text == text
True
>>> n_mlt.labels == norm_labels
True
>>> fft = FromFastText(cache_labels=True)
>>> norm_mlt = fft.format(mlt)
>>> norm_mlt.text == text
True
>>> norm_mlt.labels == labels
True
>>> tft = ToFastText(normalize_labels=True, word_seq = True, cache_labels=True)
>>> to_mlt = tft.format(norm_mlt)
>>> to_mlt.text == text
True
>>> to_mlt.labels == ft_labels_2
True
>>>
>>> nft = Normalizer(normalize_labels=True, word_seq=True, cache_labels=False)
>>> n_mlt = nft.format(norm_mlt)
>>> n_mlt.text == text
True
>>> n_mlt.labels == norm_labels
True

"""


import re
from common.prepro import normalize_label, normalize_text


class MultiLabelText:
    def __init__(self, text='', idstr=None):
        self.text = text
        self.idstr = idstr
        self.labels = set()

    def set_id(self, idstr):
        self.idstr = idstr

    def set_text(self, text):
        self.text = text

    def add_word(self, word):
        self.text += (' ' + word)

    def add_label(self, label):
        self.labels.add(label)


class Formatter:
    def __init__(self, cache_labels=False):
        self.cache_labels = cache_labels
        if cache_labels:
            self.cached_labels = {}

    def format_label(self, label):
        return label

    def format_text(self, text):
        return text

    def format(self, mlt):
        for_mlt = MultiLabelText(self.format_text(mlt.text), mlt.idstr)
        for lab in mlt.labels:
            if self.cache_labels:
                can_lab = self.cached_labels.get(lab)
                if not can_lab:
                    can_lab = self.format_label(lab)
                self.cached_labels[lab] = can_lab
            else:
                can_lab = self.format_label(lab)
            for_mlt.add_label(can_lab)
        return for_mlt


class FromFastText(Formatter):
    def __init__(self, cache_labels=False):
        super(self.__class__, self).__init__(cache_labels)

    def format_label(self, label):
        return re.sub(r'^__label__', '', label)


class ToFastText(Formatter):
    def __init__(self,
                 normalize_labels,
                 word_seq,
                 cache_labels=False):
        self.normalize_labels = normalize_labels
        self.word_seq = word_seq
        super(self.__class__, self).__init__(cache_labels)

    def format_label(self, label):
        return '__label__' + normalize_label(label, self.normalize_labels)

    def format_text(self, text):
        return normalize_text(text, self.word_seq)


class Normalizer(Formatter):
    def __init__(self,
                 normalize_labels,
                 word_seq,
                 cache_labels=False):
        self.normalize_labels = normalize_labels
        self.word_seq = word_seq
        super(self.__class__, self).__init__(cache_labels)

    def format_label(self, label):
        return normalize_label(label, self.normalize_labels)

    def format_text(self, text):
        return normalize_text(text, self.word_seq)
