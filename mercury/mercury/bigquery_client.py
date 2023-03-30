from google.cloud import bigquery

from mercury.settings import Settings
import datetime
from mercury.dto import CodeExecutionDTO
import logging

logger = logging.getLogger(__name__)


class BigqueryClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.bigquery_client = bigquery.Client()

    @property
    def dataset_id(self):
        return self.settings.bigquery_dataset_id

    @property
    def executions_table_id(self):
        return self.settings.executions_table_id

    @property
    def chatgpt_table_id(self):
        return self.settings.chat_table_id

    def get_5_last_executed_code(self) -> list[CodeExecutionDTO]:
        query = f"""
            SELECT input, output, error_output, timestamp
            FROM `{self.dataset_id}.{self.executions_table_id}`
            ORDER BY timestamp DESC
            LIMIT 5
        """
        query_job = self.bigquery_client.query(query)
        results = query_job.result()

        return [CodeExecutionDTO.from_bigquery_row(row) for row in results]

    def insert_execution_record(self, data: CodeExecutionDTO):
        table_ref = self.bigquery_client.dataset(self.dataset_id).table(
            self.executions_table_id
        )
        table = self.bigquery_client.get_table(table_ref)

        rows_to_insert = [
            {
                "input": data.code,
                "output": data.output,
                "error_output": data.error_output,
                "timestamp": datetime.datetime.now(),
            }
        ]

        errors = self.bigquery_client.insert_rows(table, rows_to_insert)

        if errors:
            logger.error(f"Error inserting rows: {errors}")
        else:
            logger.info("Inserted execution record successfully.")

    def insert_chat_record(self, prompt, response):
        table_ref = self.bigquery_client.dataset(self.dataset_id).table(
            self.chatgpt_table_id
        )
        table = self.bigquery_client.get_table(table_ref)

        rows_to_insert = [
            {
                "prompt": prompt,
                "response": response,
                "timestamp": datetime.datetime.now(),
            }
        ]

        errors = self.bigquery_client.insert_rows(table, rows_to_insert)

        if errors:
            logger.error(f"Error inserting rows: {errors}")
        else:
            logger.info("Inserted chat record successfully.")
