resource "google_cloud_scheduler_job" "every_minute_chatgpt" {
  name     = "every-minute-chatgpt"
  schedule = "*/1 * * * *"
  http_target {
    uri = google_cloudfunctions_function.chatgpt_scheduler.https_trigger_url
    http_method = "GET"
  }
}