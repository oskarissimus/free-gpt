
resource "google_pubsub_topic" "chatgpt_topic" {
  project = var.project_id
  name    = "chatgpt-topic"
}
