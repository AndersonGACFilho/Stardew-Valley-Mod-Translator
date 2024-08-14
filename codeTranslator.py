from google.cloud import translate_v2 as translate
import json
import os

# Configure your Google API Client
def create_translate_client():
    return translate.Client()

def traduzir_texto(client, texto, idioma_destino='pt-BR'):
    response = client.translate(texto, target_language=idioma_destino)
    return response['translatedText']

def traduzir_json(client, json_data, idioma_destino='pt-BR'):
    for chave, valor in json_data.items():
        if isinstance(valor, str):
            traduzido = traduzir_texto(client, valor, idioma_destino)
            json_data[chave] = traduzido
        elif isinstance(valor, dict):
            traduzir_json(client, valor, idioma_destino)
        elif isinstance(valor, list):
            for i in range(len(valor)):
                if isinstance(valor[i], str):
                    valor[i] = traduzir_texto(client, valor[i], idioma_destino)
                elif isinstance(valor[i], dict):
                    traduzir_json(client, valor[i], idioma_destino)
    return json_data

# Initialize Google Cloud Translation Client
client = create_translate_client()

# Load JSON from a file
with open('default.json', 'r', encoding='utf-8') as f:
    conteudo = f.read()

# Convert JSON content to Python dictionary
dados_json = json.loads(conteudo)

# Translate the JSON
json_traduzido = traduzir_json(client, dados_json, idioma_destino='pt-BR')

# Save the translated JSON to a new file
with open('arquivo_traduzido.json', 'w', encoding='utf-8') as f:
    json.dump(json_traduzido, f, ensure_ascii=False, indent=4)

print("Tradução concluída e salva em 'arquivo_traduzido.json'")
