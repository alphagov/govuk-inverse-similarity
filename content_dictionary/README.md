# Education theme content dictionary

This has been superceeded by the `content_dictionary.py` tool in the `../sample_spreadsheet_generator/` folder.

## Get you some data:

```
$ bundle install
$ ./content_dictionary.sh
```

Unless you have a copy of the content dictionary already, this may take a while as it scrapes the hell out of the content store.

The outcome is a 26MB json file containing everything we need to get started, dumped into your console.
You can also access the json directly through `../data/education_content_dictionary.json`

Out of politeness, I've added the `../data/pages/` folder to .gitignore
