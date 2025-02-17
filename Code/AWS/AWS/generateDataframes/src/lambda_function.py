import json
import boto3
import time
import pandas as pd
from io import StringIO

# Initialisierung des Step Functions Clients
client = boto3.client('stepfunctions')

# S3-Client initialisieren
s3 = boto3.client('s3')

# ARN der State Machine
state_machine_arn = 'arn:aws:states:eu-central-1:430118850455:stateMachine:MyStateMachine-cwuhtcehm'

# Konfigurationswerte
k_values = [2, 5, 10]
maxsup_values = [0, 10, 100]
#k_values = [2]
#maxsup_values = [10]

# Liste für die Ergebnisse
results = []

def lambda_handler(event, context):
    # TODO implement
    print(results)
    # Schleife über alle Konfigurationen
    for maxsup in maxsup_values:
        for k in k_values:
            # Konfiguration für diesen Durchlauf
            config = {
                "config": {
                    "k": k,
                    "maxsup": maxsup,
                    "samarati": True,
                    "optimal_samarati": True
                }
            }
        
            # Startzeit der Ausführung
            start_time = time.time()
        
            # Ausführung der State Machine
            response = client.start_execution(
                stateMachineArn=state_machine_arn,
                input=json.dumps(config)
            )
        
            # Warten auf Abschluss der Ausführung
            execution_arn = response['executionArn']
            while True:
                execution_response = client.describe_execution(executionArn=execution_arn)
                if execution_response['status'] == 'SUCCEEDED':
                    break
                time.sleep(1)  # Kurze Pause, um die API nicht zu überlasten
        
            # Endzeit der Ausführung
            end_time = time.time()
        
            # Laufzeit berechnen
            run_time = end_time - start_time
        
            # Ergebnis extrahieren
            output = json.loads(execution_response['output'])
            body = json.loads(output['body'])

            vector_as_string = str(body['vector']).replace('[', '(').replace(']', ')')

            # Ergebnis zur Liste hinzufügen
            results.append({
                "k": body['k'],
                "sup": body['sup'],
                "maxSup": body['maxSup'],
                "time_s": run_time,
                "loss_metric": body['loss_metric'],
                "vector": vector_as_string
                #"vector": body['vector']
            })

    # Ausgabe der Ergebnisse
    #for result in results:
    #    print(result)

    df = pd.DataFrame(results)
    print(df)

    # DataFrame in CSV umwandeln
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    # CSV-Datei in den S3-Bucket hochladen
    bucket_name = 'samarati'
    file_name = 'dataframes/DF-AWS-10k_3QI_output_1.csv'
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': json.dumps('It worked!')
    }
