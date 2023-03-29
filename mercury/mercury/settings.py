from pydantic import BaseSettings


class Settings(BaseSettings):
    bigquery_dataset_id: str
    executions_table_id: str
    chat_table_id: str
    instance_ip: str
    private_key_content: str
    instance_username: str
    gcs_bucket_name: str
    openai_api_key: str
