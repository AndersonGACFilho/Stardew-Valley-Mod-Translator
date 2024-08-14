# Stardew Valley Mod Translation Tool

## Overview

This tool is designed to translate JSON files using the Google Cloud Translation API. It is specifically useful for translating mods for Stardew Valley, making it easier to localize content for different languages.

## Requirements

- Python 3.12 or later
- `google-cloud-translate` Python package
- Google Cloud credentials

## Setup

### 1. **Install Dependencies**

Ensure you have the required Python packages installed. You can install them using pip:

```bash
pip install google-cloud-translate
```

### 2. **Set Up Google Cloud Credentials**

You need to authenticate your Google Cloud API client. Follow these steps:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a service account and download the JSON key file.
3. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your JSON key file:

   **On Windows:**
   ```cmd
   set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your-service-account-file.json
   ```

   **On macOS/Linux:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-file.json"
   ```

## Usage

### 1. **Prepare Your JSON File**

Ensure your JSON file (e.g., `default.json`) is formatted correctly and contains the text you want to translate.

### 2. **Run the Translation Script**

Execute the script to translate your JSON file:

```bash
python translate_mods.py
```

### 3. **Output**

The translated JSON will be saved to a new file named `translated_file.json`.

## Script Overview

- **`create_translate_client()`**: Initializes the Google Cloud Translation client.
- **`translate_text(client, text, target_language)`**: Translates a single string of text to the specified target language.
- **`translate_json(client, json_data, target_language)`**: Recursively translates text within a JSON object.

## Example

```python
from google.cloud import translate_v2 as translate
import json
import os

def create_translate_client():
    return translate.Client()

def translate_text(client, text, target_language='pt-BR'):
    response = client.translate(text, target_language=target_language)
    return response['translatedText']

def translate_json(client, json_data, target_language='pt-BR'):
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

client = create_translate_client()

with open('default.json', 'r', encoding='utf-8') as f:
    content = f.read()

json_data = json.loads(content)

translated_json = translate_json(client, json_data, target_language='pt-BR')

with open('translated_file.json', 'w', encoding='utf-8') as f:
    json.dump(translated_json, f, ensure_ascii=False, indent=4)

print("Translation complete and saved to 'translated_file.json'")
```

## Troubleshooting

- **Credential Errors**: Ensure that the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set correctly and that the JSON key file is valid.
- **Dependency Issues**: Make sure you have all required Python packages installed and updated.
