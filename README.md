## Generate a reference dataset

This will be a random sampling of the content dictionary to give us an idea of baseline performance.

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


