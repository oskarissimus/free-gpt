import random
import re
from typing import Optional

import tiktoken


def extract_code(input: str) -> list[str]:
    # Split the input string on the code block delimiter ('```')
    splitted = input.split('```')

    # Extract the text from every other element of the split string
    code_blocks = [splitted[i] for i in range(1,len(splitted),2)]

    # Remove any leading/trailing whitespace from each code block
    code_blocks = [block.strip() for block in code_blocks]

    # Remove any empty code blocks
    code_blocks = [block for block in code_blocks if len(block) > 0]

    # Return the list of extracted code blocks
    return code_blocks




def count_tokens(text: str) -> Optional[int]:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))


def omit_lines(text: str) -> str:
    if text is None or len(text) == 0:
        return ""
    lines = text.splitlines()
    if len(lines) <= 10:
        return text
    top = lines[:5]
    bottom = lines[-5:]
    omitted_count = len(lines) - 10
    omitted = [f"(*** {omitted_count} lines omitted ***)"]
    return "\n".join(top + omitted + bottom)


def trim_all_lines(text: str):
    lines = text.splitlines()
    return "\n".join([line.strip() for line in lines])


def remove_random_tokens_from_line(text, keep=0.9):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)
    tokens_to_keep = int(len(tokens) * keep)
    indexes_to_keep = random.sample(range(len(tokens)), tokens_to_keep)
    indexes_to_keep.sort()
    return encoding.decode([tokens[i] for i in indexes_to_keep])


def remove_random_tokens_by_percent(text, keep=0.9):
    lines = text.splitlines()
    return "\n".join(
        [remove_random_tokens_from_line(line, keep) for line in lines]
    )


def remove_random_tokens_by_count(text, keep=3000):
    if count_tokens(text) <= keep:
        return text
    keep_percent = min(1, keep / count_tokens(text))
    return remove_random_tokens_by_percent(text, keep_percent)


def digest_output_for_openai(command: str, output: str, summarize):
    output_with_ommited_lines = omit_lines(output)
    summary = summarize(command, output)
    return f"{output_with_ommited_lines}\n===> summary: {summary}"
