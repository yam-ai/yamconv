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

import sys
import getopt
import logging
from conv.multilabeltext.io import FastText2SQLite, SQLite2FastText
from common.ex import YamconvError

NUM_LINES = 1000
CACHE_LABELS = True


def main(argv):
    progname = argv[0]
    log_level = logging.WARN
    convert = None
    try:
        opts, _ = getopt.getopt(argv[1:], 'i:o:c:v')
        for opt, arg in opts:
            if opt == '-i':
                infile = arg
                continue
            if opt == '-o':
                outfile = arg
                continue
            if opt == '-c':
                convert = arg
                continue
            if opt == '-v':
                log_level = logging.INFO
                continue
    except Exception as e:
        usage(progname, e)
    logger = get_logger(log_level)
    if convert == 'fasttext2sqlite':
        converter = FastText2SQLite(
            infile, outfile, cache_labels=CACHE_LABELS,
            logger=logger, log_level=log_level, nlines=NUM_LINES)
    elif convert == 'sqlite2fasttext':
        converter = SQLite2FastText(
            infile, outfile, cache_labels=CACHE_LABELS,
            logger=logger, log_level=log_level, nlines=NUM_LINES)
    else:
        usage(progname,
              Exception('Unknown converter name {}'.format(convert)))
    try:
        converter.convert()
    except YamconvError as e:
        print('Failed to convert data: {}'.format(e), file=sys.stderr)


def get_logger(log_level):
    ch = logging.StreamHandler()
    ch.setFormatter(
        logging.Formatter(
            '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
            '%Y-%m-%d %H:%M:%S %z')
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(ch)
    logger.setLevel(log_level)
    return logger


def usage(progname, e=None):
    converter_names = ['fasttext2sqlite', 'sqlite2fasttext']
    print('Usage: {} -c converter_name -i input_file -o ouput_file -v'.format(progname),
          file=sys.stderr)
    print('-c: converter name', file=sys.stderr)
    print('-i: input file path', file=sys.stderr)
    print('-o: output file path', file=sys.stderr)
    print('-v: verbose', file=sys.stderr)
    print('Supported converters: {}'.format(
        ', '.join(converter_names)), file=sys.stderr)
    if e:
        print('Error: {}'.format(e), file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
