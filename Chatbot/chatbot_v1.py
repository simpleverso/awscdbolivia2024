import os
import json
import boto3

model_id = 'meta.llama2-13b-chat-v1'
bedrock = boto3.client(service_name='bedrock-runtime')

def lambda_handler(event, context):
    if (event['httpMethod'] == 'GET'): #Para todas las solicitudes GET, cargamos el contenido HTML desde index.html y lo devolvemos al solicitante.
        output = load_html()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': output
        }
    elif (event['httpMethod'] == "POST"): #Para todas las solicitudes POST, extraemos el cuerpo de la solicitud, lo usamos como prompt para invocar un modelo base
        body = json.loads(event['body'])
        messages = body['messages']
        print(messages)
        output = chat(messages)
        return { #, y luego devolvemos la respuesta del modelo base al solicitante.
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': output
        }
    else:
         return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': "OK" #Para todas las demás solicitudes, simplemente devolvemos un OK al solicitante.
        }

def load_html():
    html = ''
    with open('index.html', 'r') as file:
        html = file.read()
    return html

def chat(messages):
    inference_config = {'temperature': 0.5, 'topP': 1.0, 'maxTokens': 1024}
    response = bedrock.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig=inference_config
    )
    content = response['output']['message']['content']
    output = ''
    for item in content:
        output = output + item['text'] + '\n'
    return output




