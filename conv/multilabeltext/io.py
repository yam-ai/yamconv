from abc import ABC
from conv.multilabeltext.formatter import MultiLabelText, FromFastText, Normalizer, Formatter, ToFastText
import sqlite3


class Converter:
    def __init__(self, reader, from_formatter, writer, to_formatter):
        self.reader = reader
        self.from_formatter = from_formatter
        self.writer = writer
        self.to_formatter = to_formatter

    def convert(self):
        self.reader.open()
        self.writer.open()
        while True:
            from_mlt = self.reader.read()
            if not from_mlt:
                break
            norm_mlt = self.from_formatter.format(from_mlt)
            to_mlt = self.to_formatter.format(norm_mlt)
            self.writer.write(to_mlt)
        self.reader.close()
        self.writer.close()


class Reader(ABC):
    def open():
        pass

    def read():
        pass

    def close():
        pass


class Writer(ABC):
    def open():
        pass

    def write(mlt):
        pass

    def close():
        pass


class FastTextReader(Reader):
    def __init__(self, fasttext_path):
        self.fasttext_path = fasttext_path

    def open(self):
        self.fasttext_file = open(self.fasttext_path, 'r')

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
        self.fasttext_path = fasttext_path

    def open(self):
        self.fasttext_file = open(self.fasttext_path, 'w')

    def write(self, mlt):
        print(' '.join(mlt.labels + [mlt.text]), file=self.fasttext_file)

    def close(self):
        self.fasttext_file.close()


class SQLiteReader(Reader):
    def __init__(self, sqlite_path):
        self.sqlite_path = sqlite_path

    def open(self):
        self.conn = sqlite3.connect(self.sqlite_path)
        self.cur = self.conn.cursor()
        self.cur.execute('SELECT id FROM texts')
        rows = self.cur.fetchall()
        self.text_ids = [row[0] for row in rows]

    def read(self):
        try:
            text_id = self.text_ids.pop()
        except TypeError:
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
        self.sqlite_path = sqlite_path

    def open(self):
        self.conn = sqlite3.connect(self.sqlite_path)
        self.cur = self.conn.cursor()
        self.cur.executescript(schema)
        self.text_id = 0

    def write(self, mlt):
        self.cur.execute(
            'INSERT INTO texts (id, text) VALUES (?, ?)', (text_id, mlt.text))
        for label in mlt.labels:
            self.cur.execute(
                'INSERT INTO labels (label, text_id) VALUES (?, ?)', (text_id, label))

    def close(self):
        self.conn.commit()
        self.conn.close()


class FastText2SQLite(Converter):
    def __init__(self, fasttext_path, sqlite_path, cache_label=True):
        reader = FastTextReader(fasttext_path)
        from_formatter = FromFastText(cache_label=cache_label)
        writer = SQLiteWriter(sqlite_path)
        to_formatter = Normalizer(cache_label=cache_label)
        super(self.__class__, self).__init__(
            reader, from_formatter, writer, to_formatter)


class SQLite2FastText(Converter):
    def __init__(self, sqlite_path, fasttext_path, cache_label=True):
        reader = SQLiteReader(sqlite_path)
        from_formatter = Formatter(cache_label=cache_label)
        writer = FastTextWriter(fasttext_path)
        to_formatter = ToFastText(cache_label=cache_label)
        super(self.__class__, self).__init__(
            reader, from_formatter, writer, to_formatter)
