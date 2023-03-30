import json
from google.cloud import bigquery
from mercury.base_bigquery_client import BaseBigqueryClient
from mercury.settings import Settings
import datetime


class BigqueryClient(BaseBigqueryClient):
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

    def get_5_last_executed_code(self):
        query = f"""
            SELECT input, output, error_output, timestamp
            FROM `{self.dataset_id}.{self.executions_table_id}`
            ORDER BY timestamp DESC
            LIMIT 5
        """
        query_job = self.bigquery_client.query(query)
        results = query_job.result()

        last_executed_codes = []
        for row in results:
            data = {
                "input": row["input"],
                "output": row["output"],
                "error_output": row["error_output"],
                "timestamp": str(row["timestamp"]),
            }
            last_executed_codes.append(data)

        output = json.dumps(last_executed_codes)

        return output if output else "..."

    def insert_execution_record(self, input_code, output, error_output):
        table_ref = self.bigquery_client.dataset(self.dataset_id).table(
            self.executions_table_id
        )
        table = self.bigquery_client.get_table(table_ref)

        rows_to_insert = [
            {
                "input": input_code,
                "output": output,
                "error_output": error_output,
                "timestamp": datetime.datetime.now(),
            }
        ]

        errors = self.bigquery_client.insert_rows(table, rows_to_insert)

        if errors:
            print(f"Error inserting rows: {errors}")
        else:
            print("Inserted execution record successfully.")

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
            print(f"Error inserting rows: {errors}")
        else:
            print("Inserted chat record successfully.")
