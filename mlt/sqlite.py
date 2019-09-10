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

import os
import sqlite3
from common.ex import YamconvError
from mlt.mlt import gen_id, MultiLabelText, Reader, Writer


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
        self.cur.execute('SELECT DISTINCT label FROM labels ORDER BY label')
        rows = self.cur.fetchall()
        self.labels = [row[0] for row in rows]

    def read(self):
        try:
            text_id = self.text_ids.pop()
        except:
            return None
        self.cur.execute(
            'SELECT text FROM texts WHERE id = ?', (text_id, ))
        row = self.cur.fetchone()
        mlt = MultiLabelText(row[0], text_id)
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
