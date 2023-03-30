from abc import ABC, abstractmethod


class BaseBigqueryClient(ABC):
    @property
    @abstractmethod
    def dataset_id(self):
        pass

    @property
    @abstractmethod
    def executions_table_id(self):
        pass

    @abstractmethod
    def get_5_last_executed_code(self):
        """
        Retrieve the last executed code from the BigQuery table.

        Returns:
            str: The last executed code as a string, or "..." if no code was found.
        """

    @abstractmethod
    def insert_execution_record(self, input_code, output, error_output):
        """
        Insert an execution record into the BigQuery table.

        Args:
            input_code (str): The executed code.
            output (str): The output from executing the code.
            error_output (str): The error output from executing the code.
        """
