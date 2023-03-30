import json
from mercury.dto import CodeExecutionDTO
from mercury.settings import Settings
from mercury.bigquery_client import BigqueryClient
from mercury.ssh_client import SshClient
from mercury.openai_client import INTERACTION_USER_MESSAGE_TEMPLATE, OpenaiClient
from mercury.utils import extract_code, digest_output_for_openai
import logging


settings = Settings()
bigquery_client = BigqueryClient(settings)
ssh_client = SshClient(settings)
openai_client = OpenaiClient(settings)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def chatgpt_scheduler(event, context):
    logger.info("Function triggered by scheduler")
    last_executions = bigquery_client.get_5_last_executed_code()
    digested_last_executions = []
    for execution in last_executions:
        output = digest_output_for_openai(
            execution.code, execution.output, openai_client.summarize_command_output
        )
        error_output = digest_output_for_openai(
            execution.code,
            execution.error_output,
            openai_client.summarize_command_output,
        )
        digested_last_executions.append(
            CodeExecutionDTO(
                code=execution.code,
                output=output,
                error_output=error_output,
                timestamp=execution.timestamp,
            ).dict()
        )

    serialized_last_executions = json.dumps(digested_last_executions)

    prompt = INTERACTION_USER_MESSAGE_TEMPLATE.format(output=serialized_last_executions)
    chatgpt_response = openai_client.get_chatgpt_response(prompt)
    bigquery_client.insert_chat_record(prompt, chatgpt_response)
    code_snippets = extract_code(chatgpt_response)
    logger.info(f"Code snippets extracted from response: {code_snippets}")

    for code in code_snippets:
        logger.info(f"Executing code: {code}")
        output, error_output = ssh_client.execute_code(code)
        bigquery_client.insert_execution_record(code, output, error_output)

    return "Function executed successfully.", 200
