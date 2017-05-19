import random_sampler as rs

rounds = 10000

print
print 'Analysis of Education themed content.'
print 'Baseline for optimal content-ordering experiment.'
print 'For ', rounds, 'rounds of randomly ordered pages:'
print

averaged_result = rs.get_averaged_result(rounds)
rs.print_percentiles(averaged_result, [0.5, 0.8, 0.9, 0.95])
