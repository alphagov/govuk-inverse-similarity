# Tool to create sample spreadsheet for thematic analysis

In order to maximise the time-effectiveness of early-stage taxonomy generation,
this tool will create a list of conceptually-dense pages for expert review.

## Why use this tool?

Based on a review of the Education themed content, this algorithm performed significantly better than other sampling approaches when selecting for conceptual density.

## Getting set up to use the tool

First, you'll need to install some dependencies. It's a python thing, so:

```
$ git clone git@github.com:alphagov/ordering-documents-by-inverse-similarity.git
$ cd ordering-documents-by-inverse-similarity
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

We use a python library called `nltk` for natural language processing. We need a
module from `nltk` that doesn't come bundled with the library. In order to
install that module do the following:

1) Open a python console

```
$ python
Python 2.7.12 (default, Jun 29 2016, 14:05:02)
[GCC 4.2.1 Compatible Apple LLVM 7.3.0 (clang-703.0.31)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
```

2) Import `nltk` and open its package application:

```
>>> import nltk
>>> nltk.download()
showing info https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/index.xml
```

3) On the GUI it opened, click on `corpora` and scroll down until you find a
package named `stopwords`. Download that package and exit the app.


## Create a sample spreadsheet for a new theme

The process begins with consuming a list of content base paths. You'll need to create one of these. It should be a file containing a single base path per line, and the tool expects that the referenced content will be of a single theme.

For example:
```
/guidance/brucellosis
/horse-passport
/report-dead-animal
```

This file should be named `{THEME_NAME}_basepaths.csv` and saved in the `data` directory.

The first time you run the script with a new theme it will download the information it needs from the content-store. You can set the url of the content-store to use with the `--remote` CLI switch, which defaults to the live app at `https://www.gov.uk/api/content`. You can also set the `niceness` which is the time in milliseconds between API reequests. It defaults to 10.

All the CLI options are shown by running the `sample_spreadsheet_generator.py` script with `-h`

Because every step of the process is extremely time-consuming, the script will save it's intermediate workings in the data directory. Next time you run the script, it will resume where it left off.

```
./sample_spreadsheet_generator.py --theme-name environment_theme
```
