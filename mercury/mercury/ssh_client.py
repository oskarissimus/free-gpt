import paramiko
from io import StringIO
from mercury.settings import Settings
import logging
from mercury.dto import CodeExecutionDTO


logger = logging.getLogger(__name__)


class SshClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    @property
    def private_key(self) -> paramiko.RSAKey:
        return paramiko.RSAKey.from_private_key(
            StringIO(self.settings.private_key_content)
        )

    def execute_code(self, code: str) -> CodeExecutionDTO:
        try:
            self.connect_to_instance()
            return self.run_command(code)
        except Exception as e:
            logger.error(f"Error executing code: {e}")
        finally:
            self.ssh.close()

    def connect_to_instance(self) -> None:
        self.ssh.connect(
            self.settings.instance_ip,
            username=self.settings.instance_username,
            pkey=self.private_key,
        )

    def run_command(self, code: str) -> CodeExecutionDTO:
        channels_tuple = self.ssh.exec_command(code)
        return CodeExecutionDTO.from_channels_tuple_and_code(channels_tuple, code)
