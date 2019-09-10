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

from uuid import uuid4
from common.ex import YamconvError
from abc import ABC
import logging


def gen_id():
    return uuid4().hex


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


class Converter:
    def __init__(self, reader, from_formatter, writer, to_formatter,
                 logger=None, nlines=1000):
        self.reader = reader
        self.from_formatter = from_formatter
        self.writer = writer
        self.to_formatter = to_formatter
        self.logger = logger
        self.nlines = nlines

    def info(self, msg):
        if self.logger:
            self.logger.info(msg)

    def err(self, msg):
        if self.logger:
            self.logger.error(msg)
        raise YamconvError(msg)

    def convert(self):
        try:
            self.reader.open()
        except Exception as e:
            self.err('Error opening input file {}: {}'.format(
                self.reader.filepath, e))
        self.info('Opened input file {}.'.format(self.reader.filepath))
        try:
            self.writer.open()
        except Exception as e:
            self.err('Error opening output file {}: {}'.format(
                self.writer.filepath, e))
        self.info('Opened output file {}.'.format(self.writer.filepath))
        i = 0
        while True:
            try:
                from_mlt = self.reader.read()
            except Exception as e:
                self.err('Error reading input file {}: {}'.format(
                    self.reader.filepath, e))
            if not from_mlt:
                break
            norm_mlt = self.from_formatter.format(from_mlt)
            to_mlt = self.to_formatter.format(norm_mlt)
            try:
                self.writer.write(to_mlt)
            except Exception as e:
                self.err('Error writing output file {}: {}'.format(
                    self.writer.filepath, e))
            i += 1
            if i % 1000 == 0:
                self.info('Processed {} records.'.format(i))
        self.info('Completed processing {} records in total.'.format(i))
        try:
            self.reader.close()
        except Exception as e:
            self.err('Error closing input file {}: {}'.format(
                self.reader.filepath, e))
        self.info('Closed input file {}.'.format(self.reader.filepath))
        try:
            self.writer.close()
        except Exception as e:
            self.err('Error closing output file {}: {}'.format(
                self.writer.filepath, e))
        self.info('Closed output file {}.'.format(self.writer.filepath))


class Reader(ABC):
    def __init__(self, filepath):
        self.filepath = filepath

    def open():
        pass

    def read():
        pass

    def close():
        pass


class Writer(ABC):
    def __init__(self, filepath):
        self.filepath = filepath

    def open():
        pass

    def write(mlt):
        pass

    def close():
        pass
