import pytest
from mercury.settings import Settings
from mercury.bigquery_client import BigqueryClient


@pytest.fixture(scope="module")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="module")
def bigquery_client() -> BigqueryClient:
    settings = Settings()
    client = BigqueryClient(settings)
    yield client


def test_insert_chat_record(bigquery_client: BigqueryClient, settings: Settings):
    # Test data
    prompt = "Test prompt"
    response = "Test response"

    # Insert the chat record
    bigquery_client.insert_chat_record(prompt, response)

    # Query the chat record from BigQuery
    query = f"""
        SELECT prompt, response, timestamp
        FROM `{settings.project_id}.{settings.bigquery_dataset_id}.{settings.chat_table_id}`
        WHERE prompt = "{prompt}" AND response = "{response}"
        ORDER BY timestamp DESC
        LIMIT 1
    """
    query_job = bigquery_client.bigquery_client.query(query)
    results = query_job.result()

    # Verify that the record exists
    results_list = list(results)
    assert len(results_list) == 1

    # Verify the values of the record
    for row in results_list:
        assert row["prompt"] == prompt
        assert row["response"] == response
