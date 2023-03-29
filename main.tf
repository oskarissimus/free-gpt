provider "google" {
  project = var.project_id
  region  = var.region
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

  environment_variables = {
    CHATGPT_API_KEY    = var.chatgpt_api_key
    GCS_BUCKET_NAME    = google_storage_bucket.chatgpt_response_bucket.name
  }

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource = "projects/${var.project_id}/topics/${google_pubsub_topic.chatgpt_topic.name}"

  }
}

resource "google_pubsub_topic" "chatgpt_topic" {
  project = var.project_id
  name = "chatgpt-topic"
}
