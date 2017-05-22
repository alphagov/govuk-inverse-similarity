import content_dictionary as cd
import pandas as pd
import matplotlib

random_sampling = cd.load_random_results()
results = pd.DataFrame(random_sampling.mean(axis=1), columns=['mean_average'])
results['min'] = random_sampling.min(axis=1)
results['max'] = random_sampling.max(axis=1)
results.plot()
