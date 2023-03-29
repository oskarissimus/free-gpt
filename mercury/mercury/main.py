import re
from google.cloud import storage
from mercury.settings import Settings
from mercury.bigquery_client import BigqueryClient
from mercury.ssh_client import SshClient
from mercury.openai_client import OpenaiClient


settings = Settings()
bigquery_client = BigqueryClient(settings)
ssh_client = SshClient(settings)
openai_client = OpenaiClient(settings)


def store_response(response_text):
    storage_client = storage.Client()
    bucket_name = settings.gcs_bucket_name
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob("chatgpt_response.txt")
    blob.upload_from_string(response_text, content_type="text/plain")


def extract_code(response_text):
    code_pattern = re.compile(r"```\n(.*?)```", re.DOTALL)
    code_matches = code_pattern.findall(response_text)
    return code_matches


def chatgpt_scheduler(event, context):
    last_executed_code = bigquery_client.get_last_executed_code()

    prompt = f"I received this code from the last execution: {last_executed_code}. Please provide me with the next code to execute to realize your goal."

    chatgpt_response = openai_client.get_chatgpt_response(prompt)
    store_response(chatgpt_response)
    code_snippets = extract_code(chatgpt_response)

    for code in code_snippets:
        output, error_output = ssh_client.execute_code(code, bigquery_client)
        bigquery_client.insert_execution_record(code, output, error_output)

    return "Function executed successfully.", 200
