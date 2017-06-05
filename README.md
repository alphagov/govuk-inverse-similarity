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
/government/publications/permeable-surfacing-of-front-gardens-guidance
/f-gas-fridges-freezers
/winter-fuel-payment
```

This file should be named `{THEME_NAME}_basepaths.csv` and saved in the `data` directory.

The first time you run the script with a new theme it will download the information it needs from the content-store. You can set the url of the content-store to use with the `--remote` CLI switch, which defaults to the live app at `https://www.gov.uk/api/content`. You can also set the `niceness` which is the time in milliseconds between API reequests. It defaults to 10.

All the CLI options are shown by running the `sample_spreadsheet_generator.py` script with `-h`

Because every step of the process is extremely time-consuming, the script will save it's intermediate workings in the data directory. Next time you run the script, it will resume where it left off.

```
./sample_spreadsheet_generator.py --theme-name environment_theme
```

To reiterate this point: it's really not unexpected for the entire process to take over 5 hours to complete. Neither the process of building a content dictionary, nor training the model are parallelised so it will peg a single CPU core to 100% but you'll still be able to use your computer. It will cane your battery though :)

## Advanced configuration

There are two variables that the least similar selection (LSS) algorithm uses, that have been exposed to the user.

The algorithm was run in test mode against the Education theme content with many different settings, and the results for comparison are in [this google doc](https://docs.google.com/a/digital.cabinet-office.gov.uk/spreadsheets/d/1ERR5GonY98l9prmPYFR5RuxC7gQShtT_aj15MPAyUzo/edit?usp=sharing)

It is not necessary to change these values, the defaults are *probably* good enough for what you're doing.

### Number of Topics

This is passed to the [LDA](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) topic modeller. It can help to think of a Topic as a machine generated Concept or Term, however the actual output is unlikely to be particularly legible to the human mind.  In the LSS algorithm, a trained LDA model is used to assign topic-groups to thematic content. The Number of Topics parameter alters the output dramatically.

### Affinity Threshold

This is used by the topic-group sampler algorithm, after the content has been topic-modelled. It describes the minimum probability that an LDA model assigned topic can have. Lower values will produce a higher volume of sampled documents, but they may be of lower quality.

## Further Reading

This project wouldn't have been feasible without the knowledge and experience of [previous GOV.UK experiments with LDA tagging](https://github.com/alphagov/govuk-lda-tagger)
