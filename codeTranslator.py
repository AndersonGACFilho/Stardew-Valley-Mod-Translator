from google.cloud import translate_v2 as translate
import json
import os

language = 'pt-BR'

# Configure your Google API Client
def create_translate_client():
    return translate.Client()

def translate_text(client, text, target_language=language):
    response = client.translate(text, target_language=target_language)
    return response['translatedText']

def translate_json(client, json_data, target_language=language):
    for key, value in json_data.items():
        if isinstance(value, str):
            translated = translate_text(client, value, target_language)
            json_data[key] = translated
        elif isinstance(value, dict):
            translate_json(client, value, target_language)
        elif isinstance(value, list):
            for i in range(len(value)):
                if isinstance(value[i], str):
                    value[i] = translate_text(client, value[i], target_language)
                elif isinstance(value[i], dict):
                    translate_json(client, value[i], target_language)
    return json_data

# Initialize Google Cloud Translation Client
client = create_translate_client()

# Load JSON from a file
with open('default.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Convert JSON content to Python dictionary
json_data = json.loads(content)

# Translate the JSON
translated_json = translate_json(client, json_data, target_language='pt-BR')

# Save the translated JSON to a new file
with open('translated_file.json', 'w', encoding='utf-8') as f:
    json.dump(translated_json, f, ensure_ascii=False, indent=4)

print("Translation completed and saved to 'translated_file.json'")
