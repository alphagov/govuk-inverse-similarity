Get you some data:

```
$ cd content_dictionary
$ bundle install
$ bundle exec ruby -r './content_dictionary' -e 'ContentDictionary.new.compile'
```

This may take a while as it scrapes the hell out of the content store.

The outcome is a 26MB json file containing everything we need to get started.
`./content_dictionary/data/education_content_dictionary.json`

Out of politeness, I've added the `content_dictionary/data/pages/` folder to .gitignore

Next, we want to generate our reference dataset. This will be a random sampling of the content dictionary to give us an idea of baseline performance.

Run the script
```
$ cd baseline_performance
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python print_baseline.py
:
```

This will run the random sampler 1000 times and print the 80th, 90th and 95th percentile results to the console.

Run `ipython --pylab -i plot_random.py` to see the results charted.


