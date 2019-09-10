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
import csv
from common.ex import YamconvError
from mlt.mlt import MultiLabelText, Reader, Writer


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


class CSVWriter(Writer):
    def __init__(self, out_path, reader, formatter):
        self.reader = reader
        self.formatter = formatter
        super(self.__class__, self).__init__(out_path)

    def open(self):
        try:
            self.labels = [self.formatter.format_label(
                l) for l in self.reader.labels]
        except:
            raise YamconvError(
                'Labels could not be aggregated by reader {}'.format(self.reader.__class__.__name__))
        if not self.labels:
            raise YamconvError(
                'No labels are given by reader {}'.format(self.reader.__class__.__name__))
        self.out_file = open(self.filepath, 'w', newline='')
        self.csv_writer = csv.writer(
            self.out_file, delimiter=',', quotechar='"',
            quoting=csv.QUOTE_NONNUMERIC)
        self.first_row = True

    def write(self, mlt):
        if self.first_row:
            if mlt.idstr:
                self.has_id = True
                row = ['id', 'text']
            else:
                self.has_id = False
                row = ['text']
            for label in self.labels:
                row.append(label)
            self.csv_writer.writerow(row)
            self.first_row = False
        if self.has_id:
            row = [mlt.idstr]
        else:
            row = []
        row.append(mlt.text)
        for label in self.labels:
            if label in mlt.labels:
                row.append(1)
            else:
                row.append(0)
        self.csv_writer.writerow(row)

    def close(self):
        self.out_file.close()
