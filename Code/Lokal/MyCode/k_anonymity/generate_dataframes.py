import timeit
import re
from main import main
from utils import default_data_config
import pandas as pd

k_values = [2,5,10]
maxsup_values = [0, 10, 100]
#k_values = [2]
#maxsup_values = [0,10]
results = []

config = {
    'optimal_samarati': True
}
config['data'] = default_data_config

for maxsup in maxsup_values:
        for k in k_values:
            config['k'] = k
            config['maxsup'] = maxsup
            config['samarati'] = True
            # count runtime & get loss metric
            start = timeit.default_timer()
            loss_metric, vector, sup = main(config)
            stop = timeit.default_timer()
            run_time = stop - start
            
            # Ergebnis in der Liste `results` speichern:
            results.append({
                "k": k,
                "sup": sup,
                "maxSup": maxsup,
                "time_s": run_time,
                "loss_metric": loss_metric,
                "vector": vector
            })
            
df = pd.DataFrame(results)
print(df)

path = config['data']['path']
match = re.search(r'/([^/]+)\.csv$', path)
extracted_part = match.group(1) if match else None

df.to_csv('dataframes/DF-Local-'+extracted_part+'.csv', index=False)