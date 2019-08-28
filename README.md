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

* `-c`: converter
* `-i`: input file path
* `-o`: output file path
* `-s`: converter settings in JSON
* `-v`: verbose

## Supported converters

The following are the supported converters:

* `mlt.fasttext2sqlite`: fastText text file to SQLite database file
* `mlt.sqlite2fasttext`: SQLite database file to fastText text file

### Settings

Settings for converters are given in the `-s` option as a JSON string, e.g., `'{"cache_labels": true}'`.

| Setting | Values | Description | Applicable converters |
|---------|--------|-------------|-----------------------|
| `cache_labels` | `true` (default), `false` | When `cache_labels` is `true`, the reformatting of the labels is cached in memory. It can be set to `false` if there is insufficient memory to cache a huge number of different labels in the dataset. | `mlt.fasttext2sqlite`, `mlt.sqlite2fasttext` |

## Supported dataset formats

### Multi-label text classificaiton

#### fastText text file

The [fastText](https://fasttext.cc) format is a text file that contains a series of lines.
Each line represents a text classified by multiple labels.
A line starts with multiple labels, followed by the text content.
Each label is marked with the `__label__` prefix and the labels are separated by a space.
The following is a fragment of an example fastText dataset file:

```text
__label__food __label__region Many people love having dim sum in Hong Kong restaurants.
__label__region __label__plant __label__business The Netherlands is the center of production for the European floral market.
```

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

## Profesional services

If you need any supporting resources or consultancy services from YAM AI Machinery, please find us at:

* https://www.yam.ai
* https://twitter.com/theYAMai
* https://www.linkedin.com/company/yamai
* https://www.facebook.com/theYAMai
* https://github.com/yam-ai
* https://hub.docker.com/u/yamai