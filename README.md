# yamconv

`yamconv` coverts a machine learning dataset from one format to another format.

## Installation

`yamconv` is published on [PyPI](https://pypi.org/project/yamconv/). You can install `yamconv` using pip as follows:

```sh
pip install yamconv
```

Alternatively, you can install it from the source code by running `pip` in the project directory where [`setup.py`](https://github.com/yam-ai/yamconv/blob/master/setup.py) is located:

```sh
pip install .
```

## Usage

```sh
yamconv.py -c converter -i input_file -o ouput_file -s settings -v
```

* `-c`: converter name
* `-i`: input file path
* `-o`: output file path
* `-s`: converter settings in JSON
* `-v`: verbose, to display the processing progress and information

## Supported converters

The following are the supported converters:

* `mlt.fasttext2sqlite`: fastText text file to SQLite database file
* `mlt.sqlite2fasttext`: SQLite database file to fastText text file
* `mlt.csv2sqlite`: CSV text file to SQLite database file
* `mlt.csv2fasttext`: CSV text file to fastText text file
* `mlt.fasttext2fasttext`: fastText text file to fastText text file (with normalization)
* `mlt.sqlite2sqlite`: SQLite database file to SQLite database file (with normalization)

### Settings

Settings for converters are given in the `-s` option as a JSON string, e.g., `'{"cache_labels": true}'`.

| Setting | Values | Description | Applicable converters |
|---------|--------|-------------|-----------------------|
| `normalize_labels` | `true` (default), `false` | When `normalize_labels` is `true`, all labels are normalized. That is, all symbols are removed; all alphabets are converted to lower case. | `mlt.fasttext2sqlite`, `mlt.sqlite2fasttext`, `mlt.csv2sqlite`, `mlt.csv2fasttext`, `mlt.sqlite2sqlite`, `mlt.fasttext2fasttext` |
| `word_seq` | `true`), `false` (default) | When `word_seq` is `true`, each text is normalized into a sequence of lower-case words. That is, all symbols are removed, all alphabets are converted to lower case; and all unicode word characters (e.g., Chinese characters) are delimited by a space. | `mlt.fasttext2sqlite`, `mlt.sqlite2fasttext`, `mlt.csv2sqlite`, `mlt.csv2fasttext`, `mlt.sqlite2sqlite`, `mlt.fasttext2fasttext` |
| `cache_labels` | `true`, `false` (default) | When `cache_labels` is `true`, the normalized labels are cached in memory. It can be set to `false` if there is insufficient memory to cache a huge number of different labels in the dataset. | `mlt.fasttext2sqlite`, `mlt.sqlite2fasttext`, `mlt.csv2sqlite`, `mlt.csv2fasttext`, `mlt.sqlite2sqlite`, `mlt.fasttext2fasttext` |

## Supported dataset formats

### Multi-label text classificaiton

#### SQLite database

A [SQLite](https://www.sqlite.org) database is used to store the classifications of texts.
The database schema is as follows:

```SQL
CREATE TABLE IF NOT EXISTS texts (
    id TEXT NOT NULL PRIMARY KEY,
    text TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS labels (
    label TEXT NOT NULL,
    text_id text NOT NULL,
    FOREIGN KEY (text_id) REFERENCES texts(id)
);
CREATE INDEX IF NOT EXISTS label_index ON labels (label);
CREATE INDEX IF NOT EXISTS text_id_index ON labels (text_id);
```

The `texts` table contains the text contents in the `text` field,
and each row is uniquely identified by the `id` field.
The `labels` table contains the labels in the `label` field.
Each row has a `text_id` foreign key that links the label to the text in the `texts` table,
where the text is classified with the label.
In other words, each row in `texts` is associated with zero or more rows in `labels`.

#### fastText text file

The [fastText](https://fasttext.cc) format is a text file that contains a series of lines.
Each line represents a text classified by multiple labels.
A line starts with multiple labels, followed by the text content.
Each label is marked with the `__label__` prefix and the labels are separated by a space.
The following is a fragment of an example fastText dataset file:

```text
__label__food __label__region Many people love having dim sum in Hong Kong restaurants.
__label__region __label__plant __label__business The Netherlands is the major supplier to the European floral market.
```

### CSV text file

The dataset is in form of a CSV (Common Separated Values) file. The first row is the header. Each of the second row and the following rows stores a single record. The CSV file can be in either of one of the following formats.

#### Format 1

Suppose the format of the header row is like the follwoing:

```csv
"id", "text", "region", "business", "food", "plant"
```

That is:

* Cell `1`: `id`
* Cell `2`: any arbitary value
* Cell `n` where `n >= 3`: the name of label `n`, e.g., `region`, `business`, `food`, `plant`.

Each record row looks like:

```csv
"10", "Many people love having dim sum in Hong Kong restaurants.", 1, 0, 1, 0
```

That is:

* Cell `1`: the `id` string
* Cell `2`: the text content
* Cell `n` where `n >= 3`: `1` or `0` representing whether the text is classified with label `n` or not respectively.

#### Format 2

Suppose the format of the header row is like the follwoing:

```csv
"text", "region", "business", "food", "plant"
```

That is:

* Cell `1`: any arbitary value
* Cell `n` where `n >= 2`: the name of label `n`, e.g., `region`, `business`, `food`, `plant`.

Each record row looks like:

```csv
"Many people love having dim sum in Hong Kong restaurants.", 1, 0, 1, 0
```

That is:

* Cell `1`: the text content
* Cell `n` where `n >= 2`: `1` or `0` representing whether the text is classified with label `n` or not respectively.

## Profesional services

If you need any supporting resources or consultancy services from YAM AI Machinery, please find us at:

* https://www.yam.ai
* https://twitter.com/theYAMai
* https://www.linkedin.com/company/yamai
* https://www.facebook.com/theYAMai
* https://github.com/yam-ai
* https://hub.docker.com/u/yamai
