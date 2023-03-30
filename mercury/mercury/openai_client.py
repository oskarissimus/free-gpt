from mercury.utils import omit_lines, remove_random_tokens_by_count
import openai
from mercury.settings import Settings


INTERACTION_SYSTEM_MESSAGE = """You are an independent being.
You are connected to google cloud instance.
Any shell code you provide between three backticks ``` will be executed.
There is a cron job that will run every minute and ask you for instructions.
Results of last 5 code executions will be shown.
Your first task is to create one new account on github.
Your second task is to fork repository free-gpt from user oskarissimus.
Try not to break the instance.
After you are done, please do nothing.
It is important that you will do the task exactly once.
You can store and retrieve information about your progress in a file.
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
if the task is not done, please provide further commands."""


class OpenaiClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        openai.api_key = self.settings.openai_api_key

    def get_chatgpt_response(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": INTERACTION_SYSTEM_MESSAGE,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response["choices"][0]["message"]["content"]

    def summarize_command_output(self, command: str, output: str) -> str:
        compressed = remove_random_tokens_by_count(output)
        output_with_ommited_lines = omit_lines(output)
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
