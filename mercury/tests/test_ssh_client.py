import pytest
from unittest.mock import MagicMock
from mercury.settings import Settings
from mercury.ssh_client import SshClient

EXAMPLE_PRIVATE_KEY = """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEA1aTd7PFwhKOGVS/ZaMdkw+0dEynTb0Tc4iwRzfB09z5GeAUEIqoy
lJ0M2izMVB6z3npTKfO+pgMPWBurpf7Jy42zjdXGLlJqUeYfYBRHppDn3syq+APLE4hMX3
++irmRFCUP8f/Zv8SNN21gybWjfHVAECZ8FplbA6g6kKD72te/ydUfZFQZmLn4OWIjM3zb
5k+thKVfrr6dWqw6KLUAWvj0wd5TYCBVdyTkbt7cHHeuhejOynFMV6ps0JwDMya0U+sR1O
aDwyNGzbim8GmG1e2XgoIaJ2d18no0XolzDAq3PRAX5Vkr8o1SxX0ugOkkCwclRtnmcQ59
QFNekp2lTQAAA8AJ1ki6CdZIugAAAAdzc2gtcnNhAAABAQDVpN3s8XCEo4ZVL9lox2TD7R
0TKdNvRNziLBHN8HT3PkZ4BQQiqjKUnQzaLMxUHrPeelMp876mAw9YG6ul/snLjbON1cYu
UmpR5h9gFEemkOfezKr4A8sTiExff76KuZEUJQ/x/9m/xI03bWDJtaN8dUAQJnwWmVsDqD
qQoPva17/J1R9kVBmYufg5YiMzfNvmT62EpV+uvp1arDootQBa+PTB3lNgIFV3JORu3twc
d66F6M7KcUxXqmzQnAMzJrRT6xHU5oPDI0bNuKbwaYbV7ZeCghonZ3XyejReiXMMCrc9EB
flWSvyjVLFfS6A6SQLByVG2eZxDn1AU16SnaVNAAAAAwEAAQAAAQAw+F9eJmFyJcFu2U7u
M3YnarxVXir2wEQZG5zhJZLJ8V5ZuFygTX7WjcEaaVZUmc0E2+kgHpy+lMj5my4XGHXM0K
gthKiuiXmRWDws27kotuJPMX6m5sevrHhFE5TrW2mjwnMLN2gECtuLruiWk6nrpzyN9yRO
UcyI5BC4gg34tTwSNUvsxe0UvYCgEhTQdCnIucyZYF/I4CUxiUzpHbTafgPDQv5YsA7e/i
giVGTLzmJyA8/lowvKcGOBoIBb9jmrn0PNfvxMUCpllI8qVpNNIgVxhq3imFp1W8rW8Hgo
j4f2z11RDUzzKT9j+7DOy946NPvUq3ZzfII4QqSuANcJAAAAgQDprL928r9EW1vYCdHKw0
HUbXmbYfKXb2FlOPgxyAbMeosU6sUhQxw4tqzqKTCZFRZawyqRTfFay8mt1aMIAcKXcP6N
e9PwrwIA3oppE8XBzZe1p54kj6I6VJQMLK2SctfFC4Esqotb2/IcRxbZfu3KnNhHVUDLGV
sG47AlwVBAUgAAAIEA9Fi8qDIRqam88PThZEBtgJfy7NlXdluYKjfXPaBXIq6gj654b0ee
UHbRTs8PpdH5qGnDnWYZqPa96p3X/BM4WuXBVUFUzHhYgqi18mhXeTqj+WvQ0BKJwbp926
JjJXZp6I99BGra8ac5fKnNETjkN/FStZ+xJM1KT3Mo+/sMYZ8AAACBAN/VRvyzGNuo3ndo
uLIXRh/iORQv+WYmmr2uh/wMZSBNgrjUtLLIVkOYLzLGNlz44GsO2TBGz2H7QAw8TxaOfM
o291ZQPbz2QejSlKvkpTJ0pgqvlpy2PyFbxNsF6vH8J/kSZ4yr+LklA7JvneaAR4Dw66aI
dk+dYFqS5wU6DQmTAAAABmRlYmlhbgECAwQ=
-----END OPENSSH PRIVATE KEY-----"""


@pytest.fixture
def settings():
    settings = Settings()
    settings.instance_ip = "127.0.0.1"
    settings.private_key_content = EXAMPLE_PRIVATE_KEY
    settings.instance_username = "username"
    return settings


@pytest.fixture
def mock_ssh(mocker):
    mock_ssh = MagicMock()
    mocker.patch("mercury.ssh_client.paramiko.SSHClient", return_value=mock_ssh)
    return mock_ssh


def test_execute_code(settings, mock_ssh):
    ssh_client = SshClient(settings)
    mock_ssh.exec_command.return_value = (
        None,
        MagicMock(read=lambda: b"output"),
        MagicMock(read=lambda: b"error_output"),
    )

    output, error_output = ssh_client.execute_code('echo "Hello, world!"')

    mock_ssh.connect.assert_called_once_with(
        settings.instance_ip,
        username=settings.instance_username,
        pkey=ssh_client.private_key,
    )
    mock_ssh.exec_command.assert_called_once_with('echo "Hello, world!"')
    assert output == "output"
    assert error_output == "error_output"
