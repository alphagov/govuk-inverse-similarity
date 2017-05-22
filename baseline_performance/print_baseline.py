import content_dictionary as cd
import pandas as pd

print
print 'Analysis of Education themed content.'
print 'Baseline for optimal content-ordering experiment.'
print 'For 500 rounds of randomly ordered pages:'
print

random_sampling = cd.load_random_results()
cd.print_percentiles(random_sampling, [0.5, 0.8, 0.9, 0.95])

