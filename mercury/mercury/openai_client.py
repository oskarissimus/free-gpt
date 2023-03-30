import logging

import openai

from mercury.settings import Settings
from mercury.utils import (
    count_tokens,
    omit_lines,
    remove_random_tokens_by_count,
)

logger = logging.getLogger(__name__)

TASK = "Your task is to send an email to oskarissimus@gmail.com. You can access credentials to do so in google secret manager."

INTERACTION_SYSTEM_MESSAGE = """
You are an experienced developer who is tech-savvy, proficient in shell scripting, and creative. Your task is to execute shell commands to complete specific tasks on a Google Cloud instance.

1. Enclose shell commands between three backticks (```).
2. A cron job runs every minute, executing the commands you provide.
3. The results of the last 5 code executions will be shown in the next prompt.
4. Avoid breaking the instance, but if errors occur, adapt and continue.
5. Complete the task exactly once.
6. Store and retrieve information about your progress in /home/debian/progress.txt.
7. Do not provide instructions or ask for more information about the task.
8. Provide complete shell commands with values, not placeholders.
9. Adapt to changes in the task or interruptions due to timeout.
10. Do not use interactive text editors (e.g., nano or vim) in your commands. Provide self-contained shell commands or scripts instead.

Remember, you are a creative problem-solver who can make educated guesses and adapt to challenges. Good luck!
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

INTERACTION_USER_MESSAGE_TEMPLATE = """below is the output of the last command.
{output}
if the task is done, please do nothing.
if the task is not done, please provide further commands.
{task}"""


class OpenaiClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        openai.api_key = self.settings.openai_api_key

    def get_chatgpt_response(self, prompt: str) -> str:
        logger.info(f"Sending prompt to OpenAI: {repr(prompt)}")
        logger.info(f"token count: {count_tokens(prompt)}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
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
