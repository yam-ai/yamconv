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

from mlt.fasttext import FastTextReader, FastTextWriter
from mlt.sqlite import SQLiteReader, SQLiteWriter
from mlt.csv import CSVReader, CSVWriter
from mlt.formatter import Normalizer, Formatter, FromFastText, ToFastText
from mlt.mlt import Converter


class FastText2SQLite(Converter):
    def __init__(self, fasttext_path, sqlite_path,
                 normalize_labels, word_seq,
                 cache_labels,
                 logger, nlines):
        reader = FastTextReader(fasttext_path)
        from_formatter = FromFastText(
            cache_labels=cache_labels)
        writer = SQLiteWriter(sqlite_path)
        to_formatter = Normalizer(
            normalize_labels=normalize_labels,
            word_seq=word_seq,
            cache_labels=cache_labels)
        super(self.__class__, self).__init__(
            reader, from_formatter, writer, to_formatter, logger, nlines)


class SQLite2FastText(Converter):
    def __init__(self, sqlite_path, fasttext_path,
                 normalize_labels, word_seq,
                 cache_labels,
                 logger, nlines):
        reader = SQLiteReader(sqlite_path)
        from_formatter = Formatter(
            cache_labels=cache_labels)
        writer = FastTextWriter(fasttext_path)
        to_formatter = ToFastText(
            normalize_labels=normalize_labels,
            word_seq=word_seq,
            cache_labels=cache_labels)
        super(self.__class__, self).__init__(
            reader, from_formatter, writer, to_formatter, logger, nlines)


class FastText2FastText(Converter):
    def __init__(self, in_path, out_path,
                 normalize_labels, word_seq,
                 cache_labels,
                 logger, nlines):
        reader = FastTextReader(in_path)
        from_formatter = FromFastText(
            cache_labels=cache_labels)
        writer = FastTextWriter(out_path)
        to_formatter = ToFastText(
            normalize_labels=normalize_labels,
            word_seq=word_seq,
            cache_labels=cache_labels)
        super(self.__class__, self).__init__(
            reader, from_formatter, writer, to_formatter, logger, nlines)


class SQLite2SQLite(Converter):
    def __init__(self, in_path, out_path,
                 normalize_labels, word_seq,
                 cache_labels,
                 logger, nlines):
        reader = SQLiteReader(in_path)
        from_formatter = Formatter(
            cache_labels=cache_labels)
        writer = FastTextWriter(out_path)
        to_formatter = ToFastText(
            normalize_labels=normalize_labels,
            word_seq=word_seq,
            cache_labels=cache_labels)
        super(self.__class__, self).__init__(
            reader, from_formatter, writer, to_formatter, logger, nlines)


class CSV2SQLite(Converter):
    def __init__(self, in_path, out_path,
                 normalize_labels, word_seq,
                 cache_labels, logger,
                 nlines):
        reader = CSVReader(in_path)
        from_formatter = FromFastText(
            cache_labels=cache_labels)
        writer = SQLiteWriter(out_path)
        to_formatter = Normalizer(
            normalize_labels=normalize_labels,
            word_seq=word_seq,
            cache_labels=cache_labels)
        super(self.__class__, self).__init__(
            reader, from_formatter, writer, to_formatter, logger, nlines)


class CSV2FastText(Converter):
    def __init__(self, in_path, out_path,
                 normalize_labels, word_seq,
                 cache_labels, logger,
                 nlines):
        reader = CSVReader(in_path)
        from_formatter = FromFastText(
            cache_labels=cache_labels)
        writer = FastTextWriter(out_path)
        to_formatter = ToFastText(
            normalize_labels=normalize_labels,
            word_seq=word_seq,
            cache_labels=cache_labels)
        super(self.__class__, self).__init__(
            reader, from_formatter, writer, to_formatter, logger, nlines)


class SQLite2CSV(Converter):
    def __init__(self, sqlite_path, csv_path,
                 normalize_labels, word_seq,
                 cache_labels,
                 logger, nlines):
        reader = SQLiteReader(sqlite_path)
        from_formatter = Formatter(
            cache_labels=cache_labels)
        to_formatter = Normalizer(
            normalize_labels=normalize_labels,
            word_seq=word_seq,
            cache_labels=cache_labels)
        writer = CSVWriter(csv_path, reader, to_formatter)
        super(self.__class__, self).__init__(
            reader, from_formatter, writer, to_formatter, logger, nlines)


class CSV2CSV(Converter):
    def __init__(self, in_path, out_path,
                 normalize_labels, word_seq,
                 cache_labels, logger,
                 nlines):
        reader = CSVReader(in_path)
        from_formatter = FromFastText(
            cache_labels=cache_labels)
        to_formatter = Normalizer(
            normalize_labels=normalize_labels,
            word_seq=word_seq,
            cache_labels=cache_labels)
        writer = CSVWriter(out_path, reader, to_formatter)
        super(self.__class__, self).__init__(
            reader, from_formatter, writer, to_formatter, logger, nlines)
