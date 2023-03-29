import paramiko
from io import StringIO
from datetime import datetime
from mercury.settings import Settings


class SshClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    @property
    def instance_ip(self) -> str:
        return self.settings.instance_ip

    @property
    def private_key_content(self) -> str:
        return self.settings.private_key_content

    @property
    def username(self) -> str:
        return self.settings.instance_username

    @property
    def private_key(self) -> paramiko.RSAKey:
        return paramiko.RSAKey.from_private_key_file(StringIO(self.private_key_content))

    def execute_code(self, code: str) -> tuple[str, str]:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.connect_to_instance(ssh)
            output, error_output = self.run_command(ssh, code)
            return output, error_output
        except Exception as e:
            print(f"Error: {e}")
        finally:
            ssh.close()

    def connect_to_instance(self, ssh: paramiko.SSHClient) -> None:
        ssh.connect(self.instance_ip, username=self.username, pkey=self.private_key)
        print(f"Connected to {self.instance_ip}")

    def run_command(self, ssh: paramiko.SSHClient, code: str) -> tuple[str, str]:
        stdin, stdout, stderr = ssh.exec_command(code)
        output = stdout.read().decode("utf-8")
        error_output = stderr.read().decode("utf-8")
        return output, error_output
