import paramiko
from io import StringIO
from mercury.settings import Settings
import logging

logger = logging.getLogger(__name__)


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
        return paramiko.RSAKey.from_private_key(StringIO(self.private_key_content))

    def execute_code(self, code: str) -> tuple[str, str]:
        logger.info(f"Executing code: {code}")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            logger.info("Connecting to instance")
            self.connect_to_instance(ssh)
            logger.info("Connected to instance successfully")
            logger.info("Running command")
            output, error_output = self.run_command(ssh, code)
            logger.info("Command executed successfully")
            return output, error_output
        except Exception as e:
            logger.error(f"Error executing code: {e}")
        finally:
            ssh.close()

    def connect_to_instance(self, ssh: paramiko.SSHClient) -> None:
        logger.info(f"Connecting to instance: {self.instance_ip}")
        ssh.connect(self.instance_ip, username=self.username, pkey=self.private_key)
        logger.info("Connected to instance successfully.")

    def run_command(self, ssh: paramiko.SSHClient, code: str) -> tuple[str, str]:
        logger.info(f"Running command: {code}")
        stdin, stdout, stderr = ssh.exec_command(code)
        output = stdout.read().decode("utf-8")
        error_output = stderr.read().decode("utf-8")
        logger.info(f"Command output: {output}")
        logger.info(f"Command error output: {error_output}")
        return output, error_output
