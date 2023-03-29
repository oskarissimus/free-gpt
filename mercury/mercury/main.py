import os
import re
import openai
from google.cloud import storage


def get_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return response["choices"][0]["message"]["content"]


def store_response(response_text):
    storage_client = storage.Client()
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob("chatgpt_response.txt")
    blob.upload_from_string(response_text, content_type="text/plain")


def extract_code(response_text):
    code_pattern = re.compile(r"```\n(.*?)```", re.DOTALL)
    code_matches = code_pattern.findall(response_text)
    return code_matches


def execute_code(code):
    # Add your implementation to execute the code in Cloud Shell.
    # You can use the Cloud Shell REST API or another method.
    pass


def chatgpt_scheduler(event, context):
    last_executed_code = "..."  # Retrieve last executed code if needed.
    prompt = f"I received this code from the last execution: {last_executed_code}. Please provide instructions or information about this code."

    chatgpt_response = get_chatgpt_response(prompt)
    store_response(chatgpt_response)
    code_snippets = extract_code(chatgpt_response)

    for code in code_snippets:
        execute_code(code)

    return "Function executed successfully.", 200
