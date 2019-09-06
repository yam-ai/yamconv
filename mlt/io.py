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

from abc import ABC
from mlt.formatter import MultiLabelText, FromFastText, Normalizer, Formatter, ToFastText
from common.ex import YamconvError
import sqlite3
import logging
import os
import csv
from uuid import uuid4


def gen_id():
    return uuid4().hex


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


class CSVReader(Reader):
    def __init__(self, csv_path):
        super(self.__class__, self).__init__(csv_path)

    def open(self):
        if not os.path.isfile(self.filepath):
            raise YamconvError(
                'Input file {} does not exists.'.format(self.filepath))
        self.csv_file = open(self.filepath, 'r')
        self.reader = csv.reader(self.csv_file)
        try:
            header = next(self.reader)
            if header[0].strip().lower() == 'id':
                self.has_id = True
            else:
                self.has_id = False
            if self.has_id:
                self.label_start = 2
            else:
                self.label_start = 1
            self.labels = header[self.label_start:]
        except Exception as e:
            raise YamconvError('Failed to read header row: {}'.format(e))
        if not self.labels:
            raise YamconvError('No labels found')

    def read(self):
        while(True):
            try:
                row = next(self.reader)
            except StopIteration as e:
                return None
            try:
                mlt = MultiLabelText(row[self.label_start - 1])
            except Exception as e:
                raise('Failed to read the text: {}'.format(e))
            if self.has_id:
                idstr = row[0]
            else:
                idstr = None
            if idstr:
                mlt.set_id(idstr)
            if len(row) <= self.label_start:
                continue
            for i, col in enumerate(row[self.label_start:]):
                if i >= len(self.labels):
                    raise YamconvError(
                        'Column {} does not contain any label in the header row: {}'.format())
                if col == '1':
                    mlt.add_label(self.labels[i])
            break
        return mlt

    def close(self):
        self.csv_file.close()


class FastTextReader(Reader):
    def __init__(self, fasttext_path):
        super(self.__class__, self).__init__(fasttext_path)

    def open(self):
        if not os.path.isfile(self.filepath):
            raise YamconvError(
                'Input file {} does not exists.'.format(self.filepath))
        self.fasttext_file = open(self.filepath, 'r')

    def read(self):
        line = self.fasttext_file.readline()
        if line == '':
            return None
        tokens = line.split()
        words = set()
        mlt = MultiLabelText()
        for token in tokens:
            is_text = False
            if not is_text:
                if token.startswith('__label__'):
                    mlt.add_label(token)
                else:
                    is_text = True
                    mlt.add_word(token)
            else:
                mlt.add_word(token)
        return mlt

    def close(self):
        self.fasttext_file.close()


class FastTextWriter(Writer):
    def __init__(self, fasttext_path):
        super(self.__class__, self).__init__(fasttext_path)

    def open(self):
        self.fasttext_file = open(self.filepath, 'w')

    def write(self, mlt):
        print(' '.join(list(mlt.labels) + [mlt.text]), file=self.fasttext_file)

    def close(self):
        self.fasttext_file.close()


class SQLiteReader(Reader):
    def __init__(self, sqlite_path):
        super(self.__class__, self).__init__(sqlite_path)

    def open(self):
        if not os.path.isfile(self.filepath):
            raise YamconvError(
                'Input file {} does not exists.'.format(self.filepath))
        self.conn = sqlite3.connect(self.filepath)
        self.cur = self.conn.cursor()
        self.cur.execute('SELECT id FROM texts')
        rows = self.cur.fetchall()
        self.text_ids = [row[0] for row in rows]

    def read(self):
        try:
            text_id = self.text_ids.pop()
        except:
            return None
        self.cur.execute('SELECT text FROM texts WHERE id = ?', (text_id, ))
        mlt = MultiLabelText(self.cur.fetchone()[0])
        self.cur.execute(
            'SELECT label FROM labels WHERE text_id = ?', (text_id, ))
        rows = self.cur.fetchall()
        for row in rows:
            mlt.add_label(row[0])
        return mlt

    def close(self):
        self.conn.close()


schema = '''
        DROP TABLE IF EXISTS texts;
        CREATE TABLE texts (
            id TEXT NOT NULL PRIMARY KEY,
            text TEXT NOT NULL
        );
        DROP TABLE IF EXISTS labels;
        CREATE TABLE labels (
            label TEXT NOT NULL,
            text_id text NOT NULL,
            FOREIGN KEY (text_id) REFERENCES texts(id)
        );
        DROP INDEX IF EXISTS label_index;
        CREATE INDEX label_index ON labels (label);
        CREATE INDEX text_id_index ON labels (text_id);
    '''


class SQLiteWriter(Writer):
    def __init__(self, sqlite_path):
        super(self.__class__, self).__init__(sqlite_path)

    def open(self):
        self.conn = sqlite3.connect(self.filepath)
        # Can use autocommit for faster performance
        # self.conn.isolation_level = None
        self.cur = self.conn.cursor()
        self.cur.executescript(schema)

    def write(self, mlt):
        idstr = mlt.idstr
        if not idstr:
            idstr = gen_id()
        while(True):
            try:
                self.cur.execute(
                    'INSERT INTO texts (id, text) VALUES (?, ?)',
                    (idstr, mlt.text, ))
                break
            except sqlite3.IntegrityError as e:
                idstr = gen_id()

        for label in mlt.labels:
            self.cur.execute(
                'INSERT INTO labels (label, text_id) VALUES (?, ?)',
                (label, idstr, ))
        self.conn.commit()  # Can omit this commit for autocommit

    def close(self):
        self.conn.commit()
        self.conn.close()


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
