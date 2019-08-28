#!/usr/bin/env python3
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
from json import loads
from mlt.io import FastText2SQLite, SQLite2FastText
from common.ex import YamconvError

NUM_LINES = 1000
CACHE_LABELS = True

MLT_FASTTEXT_TO_SQLITE = 'mlt.fasttext2sqlite'
MLT_SQLITE_TO_FASTTEXT = 'mlt.sqlite2fasttext'


def main(argv):
    progname = argv[0]
    log_level = logging.WARN
    infile, outfile, convert, settings = None, None, None, None
    try:
        opts, _ = getopt.getopt(argv[1:], 'i:o:c:s:v')
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
            if opt == '-s':
                try:
                    settings = loads(arg)
                except Exception as e:
                    raise Exception("-s settings not in JSON")
            if opt == '-v':
                log_level = logging.INFO
                continue
    except Exception as e:
        err(progname, e)
    if not infile:
        err(progname, Exception('-i is missing'))
    if not outfile:
        err(progname, Exception('-o is missing'))
    if not convert:
        err(progname, Exception('-c is missing'))
    logger = get_logger(log_level)
    try:
        converter = get_converter(
            convert, infile, outfile,
            settings, logger, NUM_LINES)
    except Exception as e:
        err(progname, e)
    if not converter:
        err(progname,
            Exception('Unknown converter name {}'.format(convert)))
    try:
        converter.convert()
    except YamconvError as e:
        print('Failed to convert data: {}'.format(e), file=sys.stderr)


def get_converter(name, infile, outfile, settings, logger, nlines):
    converter = None
    if settings is not None:
        cache_labels = settings.get('cache_labels')
        if cache_labels not in [True, False]:
            raise YamconvError('cache_labels must be true or false')
        if cache_labels is not None:
            logger.info('cache_labels = {}'.format(cache_labels))
    if name == MLT_FASTTEXT_TO_SQLITE:
        converter = FastText2SQLite(
            infile, outfile, cache_labels=CACHE_LABELS,
            logger=logger, nlines=nlines)
    elif name == MLT_SQLITE_TO_FASTTEXT:
        converter = SQLite2FastText(
            infile, outfile, cache_labels=CACHE_LABELS,
            logger=logger, nlines=nlines)
    return converter


def get_logger(log_level):
    ch = logging.StreamHandler()
    ch.setFormatter(
        logging.Formatter(
            '[%(asctime)s|%(levelname)s] %(message)s',
            '%Y-%m-%d %H:%M:%S %z')
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(ch)
    logger.setLevel(log_level)
    return logger


def err(progname, e=None):
    converter_names = [MLT_FASTTEXT_TO_SQLITE, MLT_SQLITE_TO_FASTTEXT]
    print('Usage: {} -c converter -i input_file -o ouput_file -s settings -v'.format(progname),
          file=sys.stderr)
    print('-c: converter name', file=sys.stderr)
    print('-i: input file path', file=sys.stderr)
    print('-o: output file path', file=sys.stderr)
    print('-s: converter settings in JSON', file=sys.stderr)
    print('-v: verbose', file=sys.stderr)
    print('Supported converters: {}'.format(
        ', '.join(converter_names)), file=sys.stderr)
    if e:
        print('Error: {}'.format(e), file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
