import tiktoken
from typing import Optional
import re


def extract_code(response_text):
    code_pattern = re.compile(r"```\n(.*?)```", re.DOTALL)
    code_matches = code_pattern.findall(response_text)
    return code_matches


def count_tokens(text: str) -> Optional[int]:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))
