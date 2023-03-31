provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

data "google_project" "current" {}
resource "google_cloudfunctions_function" "chatgpt_scheduler" {
  name        = "chatgpt-scheduler"
  description = "A function that interacts with ChatGPT and executes code in Cloud Shell."
  runtime     = "python310"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.chatgpt_function_bucket.name
  source_archive_object = google_storage_bucket_object.chatgpt_function_archive.name
  entry_point           = "chatgpt_scheduler"
  timeout               = 540

  environment_variables = {
    OPENAI_API_KEY      = var.openai_api_key
    INSTANCE_IP         = google_compute_instance.executor_instance.network_interface.0.access_config.0.nat_ip
    PRIVATE_KEY_CONTENT = file("gce_ssh_key")
    INSTANCE_USERNAME   = var.instance_username
    BIGQUERY_DATASET_ID = google_bigquery_dataset.chatgpt_dataset.dataset_id
    EXECUTIONS_TABLE_ID = google_bigquery_table.executions.table_id
    CHAT_TABLE_ID       = google_bigquery_table.chat.table_id
    PROJECT_ID          = data.google_project.current.project_id
  }

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = "projects/${var.project_id}/topics/${google_pubsub_topic.chatgpt_topic.name}"
  }
}
