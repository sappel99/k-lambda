import pandas as pd
import json
import boto3
from algorithms.samarati import Lattice

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    vector = event
    
    # Laden der Daten aus S3
    response = s3_client.get_object(
        Bucket='samarati',
        Key='tmp/data.json'
    )
    data = json.loads(response['Body'].read().decode('utf-8'))
    
    # Daten aus dem temporären File einlesen
    table = pd.DataFrame.from_dict(data['table'])
    k = data['k']
    maxsup = data['maxsup']
    hierarchies = data['hierarchies']
    heights = data['heights']
    leaves_num = data['leaves_num']
    quasi_id=data['quasi_id']

    # Lattice neu erstellen
    lattice = Lattice(hierarchies=hierarchies, quasi_id=quasi_id, heights=heights)
    
    valid, sup, anonymized_table = lattice.satisfies(vector=vector, k=k, table=table, maxsup=maxsup)
    
    if valid:
        # Speichern der anonymisierten Tabelle in S3
        file_name = f"tmp/{'_'.join(map(str, vector))}.json"
        s3_client.put_object(
            Bucket='samarati',
            Key=file_name,
            Body=json.dumps(anonymized_table.to_dict())
        )

    return {
        'vector': vector,
        'sup': sup,
        'valid': valid
    }
