from pydantic import BaseSettings


class Settings(BaseSettings):
    bigquery_dataset_id: str
    bigquery_table_id: str
    instance_ip: str
    private_key_content: str
    instance_username: str
    gcs_bucket_name: str
