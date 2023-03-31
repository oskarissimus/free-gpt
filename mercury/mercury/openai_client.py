import logging

import openai

from mercury.settings import Settings
from mercury.utils import (
    count_tokens,
    omit_lines,
    remove_random_tokens_by_count,
)

logger = logging.getLogger(__name__)

TASK = """Your task is to send an email to oskarissimus@gmail.com.
You can access credentials to do so in google secret manager.
projects/682396996891/secrets/gmail_username
projects/682396996891/secrets/gmail_password"""

INTERACTION_SYSTEM_MESSAGE = """As a tech-savvy developer, complete tasks on a Google Cloud instance:
- It is very important that you enclose commands between 3 backticks (```). Otherwise, they will not be executed.
- A cron job runs your commands every minute.
- Last 5 code executions appear in next prompt.
- Store progress in /home/debian/progress.txt.
- Avoid breaking instance; adapt and continue on errors.
- Complete task once with full shell commands and values.
- Adapt to changes or interruptions; no interactive text editors.
- Remember, you're a creative problem-solver who can adapt. Good luck!
- Single command should be shorter than 500 chatgpt-3.5-turbo tokens.
- Default timeout is 60 seconds. If you anticipate longer execution time, split your command into multiple steps, and execute them one by one in separate prompts.
- If the task is done, please do nothing.
- If the task is not done, please provide further commands.
{task}
"""


COMPRESSION_SYSTEM_MESSAGE = """I will show you output of shell command.
I want you to summarize it in single sentence.
No explainations, just one-sentence summarization.
It is possible that output was too long, so I removed random tokens from it.
It is improtant that you deduce the meaning of the output from the remaining tokens.
It is also important to inform about any errors that occured or success of the command.
If there is too little information, inform about that.
To make it easier for you, I will also show you first and last 5 lines of the output and the first 100 characters of the command.
"""

COMPRESSION_USER_MESSAGE_TEMPLATE = """===> command: {command}
===> compressed output: {compressed_output}
===> output with ommited lines {output_with_ommited_lines}"""

INTERACTION_USER_MESSAGE_TEMPLATE = """- Below are the outputs of the last 5 attempts.
{output}"""


class OpenaiClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        openai.api_key = self.settings.openai_api_key

    def get_chatgpt_response(self, prompt: str) -> str:
        logger.info(f"Sending prompt to OpenAI: {prompt}")
        logger.info(f"token count: {count_tokens(prompt)}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.9,
        )

        return response["choices"][0]["message"]["content"]

    def summarize_command_output(self, command: str, output: str) -> str:
        if len(output) < 100:
            return output
        compressed = remove_random_tokens_by_count(output)
        output_with_ommited_lines = omit_lines(output, 4)
        user_message = COMPRESSION_USER_MESSAGE_TEMPLATE.format(
            command=command[:100],
            compressed_output=compressed,
            output_with_ommited_lines=output_with_ommited_lines,
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": COMPRESSION_SYSTEM_MESSAGE,
                },
                {"role": "user", "content": user_message},
            ],
        )

        return response["choices"][0]["message"]["content"]
