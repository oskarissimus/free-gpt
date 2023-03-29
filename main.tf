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

  environment_variables = {
    OPENAI_API_KEY      = var.openai_api_key
    GCS_BUCKET_NAME     = google_storage_bucket.chatgpt_response_bucket.name
    INSTANCE_IP         = google_compute_instance.executor_instance.network_interface.0.access_config.0.nat_ip
    PRIVATE_KEY_CONTENT = file("gce_ssh_key")
    SSH_USERNAME        = var.instance_username
    BIGQUERY_DATASET_ID = google_bigquery_dataset.chatgpt_dataset.dataset_id
    EXECUTIONS_TABLE_ID = google_bigquery_table.executions.table_id
    CHAT_TABLE_ID       = google_bigquery_table.chat.table_id
  }

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = "projects/${var.project_id}/topics/${google_pubsub_topic.chatgpt_topic.name}"
  }
}



resource "google_pubsub_topic" "chatgpt_topic" {
  project = var.project_id
  name    = "chatgpt-topic"
}

resource "google_compute_instance" "executor_instance" {
  name         = "executor-instance"
  machine_type = "f1-micro"
  zone         = var.zone
  metadata = {
    ssh-keys = "${var.instance_username}:${file("gce_ssh_key.pub")}"
  }
  boot_disk {
    initialize_params {
      image = "projects/debian-cloud/global/images/family/debian-11"
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral external IP
    }
  }

  service_account {
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

}

resource "google_bigquery_dataset" "chatgpt_dataset" {
  dataset_id = "chatgpt_dataset"
}

resource "google_bigquery_table" "executions" {
  dataset_id = google_bigquery_dataset.chatgpt_dataset.dataset_id
  table_id   = "executions"

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
  dataset_id = google_bigquery_dataset.chatgpt_dataset.dataset_id
  table_id   = "chat"

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

