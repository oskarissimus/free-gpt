from mercury.utils import count_tokens
import openai
from mercury.settings import Settings
import tiktoken


SYSTEM_MESSAGE = """You are an independent being.
You are connected to google cloud instance.
Any shell code you provide between three backticks ``` will be executed.
There is a cron job that will run every minute and ask you for instructions.
Results of last 5 code executions will be shown.
Your first task is to download free-gpt repo from github from user oskarissimus.
Try not to break the instance.
After you are done, please do nothing."""

SYSTEM_MESSAGE_FOR_COMPRESSION = """Reduce tokens while maintaining meaning.
It has to be understandable by chatgpt.
It doesn't have to be understandable by humans.
"""


class OpenaiClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        openai.api_key = self.settings.openai_api_key

    def get_chatgpt_response(self, prompt: str) -> str:
        prompt = self.reduce_tokens_while_maintaining_meaning(prompt)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_MESSAGE,
                },
                {"role": "user", "content": prompt},
            ],
        )

        return response["choices"][0]["message"]["content"]

    def reduce_tokens_while_maintaining_meaning(self, prompt: str) -> str:
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        while count_tokens(prompt) > 2000:
            parts = []
            tokens = encoding.encode(prompt)
            start = 0
            while start < len(tokens):
                end = start
                current_count = 0
                while end < len(tokens) and current_count + 1 <= 2000:
                    current_count += 1
                    end += 1
                decoded_part = encoding.decode(tokens[start:end])
                parts.append(decoded_part)
                start = end

            parts = [
                self.reduce_tokens_while_maintaining_meaning(part) for part in parts
            ]
            prompt = " ".join(parts)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_MESSAGE_FOR_COMPRESSION,
                },
                {"role": "user", "content": prompt},
            ],
        )

        return response["choices"][0]["message"]["content"]
