import paramiko
import os
import re
import openai
from google.cloud import storage
from io import StringIO


def get_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an independent being. You are connected to google cloud instance. Any shell code you provide between three backticks ``` will be executed. There is cron job that will run every minute and ask you for instructions. Output of the code will be included in the next prompt. This is a test run. I want you to run the following code: ```echo 'Hello World'```",
            },
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
    instance_ip = os.environ.get("INSTANCE_IP")
    private_key_content = os.environ.get("PRIVATE_KEY_CONTENT")
    username = os.environ.get("INSTANCE_USERNAME")
    private_key = paramiko.RSAKey.from_private_key_file(StringIO(private_key_content))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the GCE instance
    try:
        ssh.connect(instance_ip, username=username, pkey=private_key)
        print(f"Connected to {instance_ip}")

        # Execute the code
        stdin, stdout, stderr = ssh.exec_command(code)
        output = stdout.read().decode("utf-8")
        error_output = stderr.read().decode("utf-8")

        # Print the outputs
        print("Output:")
        print(output)
        print("Error Output:")
        print(error_output)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        ssh.close()


def chatgpt_scheduler(event, context):
    last_executed_code = "..."  # Retrieve last executed code if needed.
    prompt = f"I received this code from the last execution: {last_executed_code}. Please provide instructions or information about this code."

    chatgpt_response = get_chatgpt_response(prompt)
    store_response(chatgpt_response)
    code_snippets = extract_code(chatgpt_response)

    for code in code_snippets:
        execute_code(code)

    return "Function executed successfully.", 200
