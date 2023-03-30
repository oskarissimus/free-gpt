import datetime
import json
import logging

from mercury.bigquery_client import BigqueryClient
from mercury.dto import CodeExecutionDTO
from mercury.openai_client import (
    INTERACTION_SYSTEM_MESSAGE,
    INTERACTION_USER_MESSAGE_TEMPLATE,
    TASK,
    OpenaiClient,
)
from mercury.settings import Settings
from mercury.ssh_client import SshClient
from mercury.utils import (
    count_tokens,
    digest_output_for_openai,
    extract_code,
    trim_by_token_count,
)

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
            execution.code,
            execution.output,
            openai_client.summarize_command_output,
        )
        error_output = digest_output_for_openai(
            execution.code,
            execution.error_output,
            openai_client.summarize_command_output,
        )
        digested_last_executions.append(
            CodeExecutionDTO(
                code=trim_by_token_count(execution.code, 500),
                output=output,
                error_output=error_output,
                timestamp=execution.timestamp,
            ).dict()
        )

    serialized_last_executions = json.dumps(digested_last_executions)

    prompt = (
        INTERACTION_SYSTEM_MESSAGE
        + INTERACTION_USER_MESSAGE_TEMPLATE.format(
            output=serialized_last_executions, task=TASK
        )
    )
    chatgpt_response = openai_client.get_chatgpt_response(prompt)
    bigquery_client.insert_chat_record(prompt, chatgpt_response)
    code_snippets = extract_code(chatgpt_response)
    logger.info(f"response: {repr(chatgpt_response)}")
    logger.info(f"Code snippets extracted from response: {code_snippets}")

    if count_tokens(" ".join(code_snippets)) > 500:
        logger.info("Code snippets too long, not executing.")
        bigquery_client.insert_execution_record(
            CodeExecutionDTO(
                code="Code snippets too long, not executing.",
                output="",
                error_output="",
                timestamp=datetime.datetime.now(),
            )
        )
        return "Code snippets too long, not executing.", 200

    for code in code_snippets:
        logger.info(f"Executing code: {code}")
        execution = ssh_client.execute_code(code)
        bigquery_client.insert_execution_record(execution)

    return "Function executed successfully.", 200
