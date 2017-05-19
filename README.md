## Generate a reference dataset

This will be a random sampling of the content dictionary to give us an idea of baseline performance.

Run the script
```
$ cd baseline_performance
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python print_baseline.py
```

This will run the random sampler 1000 times and print the 80th, 90th and 95th percentile results to the console.

Run `ipython --pylab -i plot_random.py` to see the results charted.

```
Analysis of Education themed content.
Baseline for optimal content-ordering experiment.
For average of 10000 rounds of randomly ordered pages:

80% of terms were found by reviewing an average of 613 pages. 8.4% of corpus, σ 90, range 299 - 1042

90% of terms were found by reviewing an average of 1229 pages. 16.8% of corpus, σ 203, range 642 - 2236

95% of terms were found by reviewing an average of 2116 pages. 29.0% of corpus, σ 382, range 962 - 2924
```
