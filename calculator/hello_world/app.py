import json

# import requests

def lambda_handler(event, context):
    """
    Lambda function que realiza operaciones matemáticas básicas
    Maneja tanto eventos simples como eventos de API Gateway
    """
    
    try:
        # Determinar el origen de los datos según el tipo de evento
        data = extract_data_from_event(event)
        
        # Extraer valores del evento
        numero1 = data.get('numero1')
        numero2 = data.get('numero2')
        funcion = data.get('funcion', '').lower()
        
        # Validar que los parámetros requeridos estén presentes
        if numero1 is None or numero2 is None or not funcion:
            return create_response(400, {
                'error': 'Parámetros requeridos: numero1, numero2, funcion'
            })
        
        # Convertir strings a enteros si es necesario
        try:
            if isinstance(numero1, str):
                numero1 = int(numero1)
            if isinstance(numero2, str):
                numero2 = int(numero2)
        except ValueError:
            return create_response(400, {
                'error': 'Los números deben ser valores numéricos válidos'
            })
            
        # Realizar la operación según la función especificada
        if funcion == 'suma':
            resultado = numero1 + numero2
        elif funcion == 'resta':
            resultado = numero1 - numero2
        elif funcion == 'multiplicacion':
            resultado = numero1 * numero2
        elif funcion == 'division':
            if numero2 == 0:
                return create_response(400, {
                    'error': 'No se puede dividir por cero'
                })
            resultado = numero1 / numero2
        else:
            return create_response(400, {
                'error': f'Función "{funcion}" no soportada. Use: suma, resta, multiplicacion, division'
            })
            
        # Retornar respuesta exitosa
        return create_response(200, {
            'resultado': resultado
        })
        
    except Exception as e:
        return create_response(500, {
            'error': f'Error interno del servidor: {str(e)}'
        })

def extract_data_from_event(event):
    """
    Extrae los datos del evento, manejando diferentes formatos:
    1. Evento simple: datos directamente en el root
    2. API Gateway con body JSON
    3. API Gateway con query parameters
    """
    
    # Si es un evento simple (tiene numero1, numero2 directamente)
    if 'numero1' in event:
        return event
    
    # Si es un evento de API Gateway
    if 'httpMethod' in event:
        # Primero intentar extraer del body (POST)
        if event.get('body'):
            try:
                return json.loads(event['body'])
            except json.JSONDecodeError:
                pass
        
        # Si no hay body válido, intentar query parameters (GET)
        if event.get('queryStringParameters'):
            return event['queryStringParameters']
    
    # Si no encuentra datos en ningún formato esperado
    return {}

def create_response(status_code, body_data):
    """
    Crea una respuesta consistente para Lambda
    """
    return {
        'statusCode': status_code,
        'body': json.dumps(body_data),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # Para CORS si se usa con API Gateway
        }
    }