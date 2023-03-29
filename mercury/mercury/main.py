from mercury.settings import Settings
from mercury.bigquery_client import BigqueryClient
from mercury.ssh_client import SshClient
from mercury.openai_client import OpenaiClient
from mercury.utils import extract_code


settings = Settings()
bigquery_client = BigqueryClient(settings)
ssh_client = SshClient(settings)
openai_client = OpenaiClient(settings)


def chatgpt_scheduler(event, context):
    last_executed_code = bigquery_client.get_last_executed_code()

    prompt = f"I received this code from the last execution: {last_executed_code}. Please provide me with the next code to execute to realize your goal."

    chatgpt_response = openai_client.get_chatgpt_response(prompt)
    bigquery_client.insert_chat_record(prompt, chatgpt_response)
    code_snippets = extract_code(chatgpt_response)

    for code in code_snippets:
        output, error_output = ssh_client.execute_code(code, bigquery_client)
        bigquery_client.insert_execution_record(code, output, error_output)

    return "Function executed successfully.", 200
