import os
import json
import re
import requests
from google.cloud import storage

def get_chatgpt_response(prompt):
    API_KEY = os.environ.get('CHATGPT_API_KEY')
    API_URL = 'https://api.openai.com/v1/engines/davinci-codex/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }

    data = {
        'prompt': prompt,
        'max_tokens': 100,
        'n': 1,
        'stop': None,
        'temperature': 1,
    }

    response = requests.post(API_URL, headers=headers, json=data)
    response_json = response.json()
    return response_json['choices'][0]['text'].strip()

def store_response(response_text):
    storage_client = storage.Client()
    bucket_name = os.environ.get('GCS_BUCKET_NAME')
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob('chatgpt_response.txt')
    blob.upload_from_string(response_text, content_type='text/plain')

def extract_code(response_text):
    code_pattern = re.compile(r'```\n(.*?)```', re.DOTALL)
    code_matches = code_pattern.findall(response_text)
    return code_matches

def execute_code(code):
    # Add your implementation to execute the code in Cloud Shell.
    # You can use the Cloud Shell REST API or another method.
    pass

def chatgpt_scheduler(request):
    last_executed_code = '...'  # Retrieve last executed code if needed.
    prompt = f"I received this code from the last execution: {last_executed_code}. Please provide instructions or information about this code."
    
    chatgpt_response = get_chatgpt_response(prompt)
    store_response(chatgpt_response)
    code_snippets = extract_code(chatgpt_response)

    for code in code_snippets:
        execute_code(code)

    return 'Function executed successfully.', 200
