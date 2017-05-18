import random_sampler as rs

rounds = 1000
averaged_result = rs.get_averaged_result(rounds)
rs.print_80_90_95th_percentiles(averaged_result, rounds)
