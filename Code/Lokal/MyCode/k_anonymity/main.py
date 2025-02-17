import argparse
from algorithms.samarati import samarati, Lattice
from utils.data_loader import load_data, build_categorical_hierarchy, build_range_hierarchy
from utils import display_table, default_data_config

import re

def main(config):
    data = load_data(config=config)
    if config['samarati']:
        hierarchies, heights, leaves_num = {}, {}, {}
        for attr, path in config['data']['hierarchies'].items():
            if config['data']['samarati_generalization_type'][attr] == 'categorical':
                hierarchies[attr], heights[attr], leaves_num[attr] = build_categorical_hierarchy(path)
            else:  # range generalization
                hierarchies[attr], heights[attr], leaves_num[attr] = build_range_hierarchy(data['table'][attr])
        print('\nhierarchies:\n', hierarchies)
        print('\nhierarchy heights:\n', heights)
        # run samarati
        lattice = Lattice(hierarchies=hierarchies, quasi_id=data['quasi_id'], heights=heights)
        anonymized_table, vector, sup, loss_metric = samarati(table=data['table'], lattice=lattice, 
                                                    k=config['k'], maxsup=config['maxsup'], 
                                                    optimal=config['optimal_samarati'],
                                                    leaves_num=leaves_num,
                                                    sensitive=config['data']['sensitive'])
        # display
        print('generalization vector:', vector)
        print('max suppression:', sup)
        anonymized_table = anonymized_table[data['quasi_id'] + [data['sensitive']]]
        display_table(anonymized_table)
        # save to file
        path = config['data']['path']
        match = re.search(r'/([^/]+)\.csv$', path)
        extracted_part = match.group(1) if match else None
        anonymized_table.columns = config['data']['samarati_quasi_id']+[config['data']['sensitive']]
        anonymized_table.to_csv('results/anonData-Local-'+extracted_part+'.csv', header=True, index=None)

    else:
        raise NotImplementedError('Algorithm not chosen. Please add argument --samarati')

    return loss_metric, vector, sup


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", default=10, type=int)
    parser.add_argument("--maxsup", default=20, type=int)
    parser.add_argument("--samarati", action='store_true')
    parser.add_argument("--optimal-samarati", action='store_true')

    config = vars(parser.parse_args())
    config['data'] = default_data_config
    print('\nconfiguration:\n', config)

    
    main(config)
