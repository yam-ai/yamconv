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
from mlt.mlt import MultiLabelText, Reader, Writer
from common.ex import YamconvError


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
