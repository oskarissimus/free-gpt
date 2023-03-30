import pytest
from mercury.settings import Settings
from mercury.openai_client import OpenaiClient
from mercury.utils import count_tokens


@pytest.fixture
def openai_client():
    settings = Settings()
    return OpenaiClient(settings=settings)


def test_reduce_tokens_while_maintaining_meaning(openai_client: OpenaiClient):
    original_prompt = "This is a sample prompt with some redundant information. The main goal of the test is to check if the 'reduce_tokens_while_maintaining_meaning' method works as expected."
    reduced_prompt = openai_client.reduce_tokens_while_maintaining_meaning(
        original_prompt
    )

    original_tokens_count = count_tokens(original_prompt)
    reduced_tokens_count = count_tokens(reduced_prompt)
    assert reduced_tokens_count < original_tokens_count

    gpt_response = openai_client.get_chatgpt_response(reduced_prompt)
    assert gpt_response is not None and len(gpt_response) > 0


def test_compression_of_prompt_over_2000_tokens(openai_client: OpenaiClient):
    long_sentence = "This is a very long prompt with many words to ensure it has more than 2000 tokens when repeated multiple times. "
    long_prompt = long_sentence * 90

    original_tokens_count = count_tokens(long_prompt)
    assert original_tokens_count > 2000

    compressed_prompt = openai_client.reduce_tokens_while_maintaining_meaning(
        long_prompt
    )

    compressed_tokens_count = count_tokens(compressed_prompt)
    assert compressed_tokens_count <= 2000

    gpt_response = openai_client.get_chatgpt_response(compressed_prompt)
    assert gpt_response is not None and len(gpt_response) > 0
