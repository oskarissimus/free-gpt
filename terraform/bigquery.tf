
resource "google_bigquery_dataset" "chatgpt_dataset" {
  dataset_id = "chatgpt_dataset"
}

resource "google_bigquery_table" "executions" {
  dataset_id          = google_bigquery_dataset.chatgpt_dataset.dataset_id
  table_id            = "executions"
  deletion_protection = false

  schema = jsonencode([
    {
      "name" : "input",
      "type" : "STRING",
    },
    {
      "name" : "output",
      "type" : "STRING",
      "mode" : "NULLABLE",

    },
    {
      "name" : "error_output",
      "type" : "STRING",
      "mode" : "NULLABLE",

    },
    {
      "name" : "timestamp",
      "type" : "TIMESTAMP",
    }
  ])
}

resource "google_bigquery_table" "chat" {
  dataset_id          = google_bigquery_dataset.chatgpt_dataset.dataset_id
  table_id            = "chat"
  deletion_protection = false

  schema = jsonencode([
    {
      "name" : "prompt",
      "type" : "STRING",
      "mode" : "NULLABLE",
    },
    {
      "name" : "response",
      "type" : "STRING",
      "mode" : "NULLABLE",
    },
    {
      "name" : "timestamp",
      "type" : "TIMESTAMP",
    }
  ])
}
