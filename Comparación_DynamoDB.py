import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('PreciosLibros')

def registrar_precio_dynamodb(libro, precio_actual, baja_precio):
    fecha = datetime.now().strftime('%Y-%m-%d')
    tabla.put_item(
        Item={
            'Libro': libro,
            'Fecha': fecha,
            'Precio': precio_actual,
            'BajaPrecio': baja_precio
        }
    )
    print(f"Datos registrados en DynamoDB para el libro '{libro}'.")

def verificar_y_registrar_precio(libro, precio_actual):
    # Obtener el precio más reciente del libro
    response = tabla.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('Libro').eq(libro),
        Limit=1,
        ScanIndexForward=False  # Último precio registrado
    )

    registros = response.get('Items', [])
    baja_precio = False

    if registros:
        precio_anterior = registros[0]['Precio']
        if precio_actual < precio_anterior:
            print(f"¡Bajada de precio para '{libro}'! Ahora: {precio_actual}, Antes: {precio_anterior}")
            baja_precio = True
        elif precio_actual > precio_anterior:
            print(f"Subida de precio para '{libro}'. Ahora: {precio_actual}, Antes: {precio_anterior}")
        else:
            print(f"El precio de '{libro}' se mantuvo igual: {precio_actual}.")
    else:
        print(f"Primer registro del libro '{libro}' con precio: {precio_actual}.")

    # Registrar en DynamoDB
    registrar_precio_dynamodb(libro, precio_actual, baja_precio)