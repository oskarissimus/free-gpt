from mercury.main import get_chatgpt_response

def test_get_chatgpt_response_integration():
    prompt = "What is the capital of France?"
    response = get_chatgpt_response(prompt)

    assert "Paris" in response
