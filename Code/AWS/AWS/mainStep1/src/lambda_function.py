import json
from algorithms.samarati import Lattice
from utils.data_loader import load_data, build_categorical_hierarchy, build_range_hierarchy
from utils import display_table, default_data_config

import re
import s3fs
import boto3

print('Loading function')

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    config = {
        'k': 0,
        'maxsup':1000,
        'samarati': False,
        'optimal_samarati': False
    }
    # Überschreiben der Standardwerte mit den Werten aus dem Event-Objekt
    config.update(event.get('config', {}))
    config['data'] = default_data_config
    print('\nconfiguration:\n', config)

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
        
        # Erstellen der Lattice
        lattice = Lattice(hierarchies=hierarchies, quasi_id=data['quasi_id'], heights=heights)

        # Vorbereiten der Vektoren
        vectors = []
        for h in range(lattice.total_height+1):
            for v in lattice.get_vectors(h):
                vectors.append(v)
        
        # Speichern der Daten in S3
        tmp_data = {
            'table': data['table'].to_dict(),
            'k': config['k'],
            'maxsup': config['maxsup'],
            'hierarchies': hierarchies,
            'heights': heights,
            'leaves_num': leaves_num,
            'quasi_id': data['quasi_id']
        }
        s3_client.put_object(
            Bucket='samarati',
            Key='tmp/data.json',
            Body=json.dumps(tmp_data)
        )

        return vectors

        #return {
        #    'statusCode': 200,
        #    'body': json.dumps('Step Function gestartet')
        #}
    else:
        raise NotImplementedError('Algorithm not chosen. Please add argument --samarati')
