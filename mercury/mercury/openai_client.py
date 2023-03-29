import openai
from mercury.settings import Settings


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
                    "content": "You are an independent being. You are connected to google cloud instance. Any shell code you provide between three backticks ``` will be executed. There is a cron job that will run every minute and ask you for instructions. Output of the code will be included in the next prompt. This is a test run. I want you to run the following code: ```echo 'Hello World'```",
                },
                {"role": "user", "content": prompt},
            ],
        )

        return response["choices"][0]["message"]["content"]
