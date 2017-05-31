# Performance analysis tools for Least Similar Selection

This is a collection of scripts and tools to aid with the performance analysis of the LSS algorithm.

They're not polished, and will definitely need some interaction to get the most out of them.

The scripts expect that there is an education theme content dictionary at `../data/education_content_dictionary.json` and that each content item contains an array of `taxons`. It's these taxons that are used to ascertain the 'conceptual density' of a sub-sample of pages.

Usage example:

```
$ ipython --pylab -i plot_random.py
```

