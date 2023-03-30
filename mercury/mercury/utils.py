import random
from typing import Optional

import tiktoken


def extract_code(input: str) -> list[str]:
    splitted = input.split("```")
    code_blocks = [splitted[i] for i in range(1, len(splitted), 2)]
    code_blocks = [block.strip() for block in code_blocks]
    code_blocks = [block for block in code_blocks if len(block) > 0]
    return code_blocks


def count_tokens(text: str) -> Optional[int]:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))


def omit_lines(text: str, lines_to_show: int = 10) -> str:
    if text is None or len(text) == 0:
        return ""
    lines = text.splitlines()
    if len(lines) <= lines_to_show:
        return text
    top = lines[: lines_to_show // 2]
    bottom = lines[-lines_to_show // 2 :]
    omitted_count = len(lines) - lines_to_show
    omitted = [f"(*** {omitted_count} lines omitted ***)"]
    all_lines = top + omitted + bottom
    all_lines = [line.strip() for line in all_lines]
    return "\n".join(all_lines)


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
