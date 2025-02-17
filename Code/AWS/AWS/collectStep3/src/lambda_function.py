import json
import boto3
import pandas as pd
from operator import itemgetter
from utils.loss_metrics import categorical_loss_metric

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    results = event if isinstance(event, list) else event.get('input', [])
    
    # Laden der zusätzlichen Daten aus S3 für die Verlustmetrik
    response = s3_client.get_object(
        Bucket='samarati',
        Key='tmp/data.json'
    )
    data = json.loads(response['Body'].read().decode('utf-8'))
    leaves_num = data['leaves_num']
    hierarchies = data['hierarchies']
    quasi_id = data['quasi_id']
    maxsup = data['maxsup']
    k = data['k']
    
    possible_solutions = []
    
    for result in results:
        if result['valid']:
            vector = result['vector']
            sup = result['sup']
            
            # Laden der anonymisierten Tabelle für diesen Vektor
            file_name = f"tmp/{'_'.join(map(str, vector))}.json"
            table_response = s3_client.get_object(
                Bucket='samarati',
                Key=file_name
            )
            anonymized_table = pd.DataFrame.from_dict(json.loads(table_response['Body'].read().decode('utf-8')))
            
            loss_metric = categorical_loss_metric(
                anonymized_table[quasi_id],
                leaves_num,
                hierarchies,
                sup
            )
            
            possible_solutions.append({
                'k': k,
                'sup': sup,
                'maxSup': maxsup,
                'loss_metric': loss_metric,
                'vector': vector
            })
    
    # Optimale Lösung finden (niedrigste Verlustmetrik)
    optimal_solution = sorted(possible_solutions, key=itemgetter('loss_metric'))[0]
    
    

    return {
        'statusCode': 200,
        'body': json.dumps(optimal_solution)
    }
