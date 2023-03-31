resource "google_cloud_scheduler_job" "every_minute_chatgpt" {
  name     = "every-minute-chatgpt"
  schedule = "*/1 * * * *"
  paused   = var.scheduler_paused
  pubsub_target {
    topic_name = "projects/${var.project_id}/topics/${google_pubsub_topic.chatgpt_topic.name}"
    data       = ""
    attributes = {
      foo = "bar"
    }
  }
}
