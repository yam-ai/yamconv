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

"""This module contains functions to clean and tokenize text.
>>> s = u'''世界，你好！
... Hello, World!
... Hëllo, Wôrld!'''
>>> remove_symbols(s)
'世界 你好  Hello  World  Hëllo  Wôrld '
>>> normalize_text(s)
'世 界 你 好 hello world hëllo wôrld'
>>> normalize_label(s)
'世界_你好_hello_world_hëllo_wôrld'
"""

import re


def remove_symbols(s):
    return re.sub(r'[^\w]', ' ', s, flags=re.UNICODE)


def normalize(s, split_unichars=False, to_lower=True, delimiter=' '):
    words = []
    word = []
    for c in s:
        if c == ' ':
            if word:
                words.append(''.join(word))
                word = []
        else:
            if split_unichars and ord(c) > 255:
                if word:
                    words.append(''.join(word))
                words.append(c)
                word = []
                continue
            if to_lower:
                c = c.lower()
            word.append(c)
    return delimiter.join(words)


def normalize_text(s):
    return normalize(remove_symbols(s), split_unichars=True)


def normalize_label(s):
    return normalize(remove_symbols(s), delimiter='_')
