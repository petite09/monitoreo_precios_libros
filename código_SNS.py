import boto3

sns = boto3.client('sns')
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:123456789012:PrecioAlertas'

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT' or record['eventName'] == 'MODIFY':
            nuevo_precio = record['dynamodb']['NewImage']['Precio']['N']
            baja_precio = record['dynamodb']['NewImage'].get('BajaPrecio', {}).get('BOOL', False)
            libro = record['dynamodb']['NewImage']['Libro']['S']

            if baja_precio:
                mensaje = f"¡Bajada de precio detectada! El libro '{libro}' ahora cuesta {nuevo_precio}."
                print(mensaje)

                # Enviar notificación
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=mensaje,
                    Subject="Bajada de Precio Detectada"
                )