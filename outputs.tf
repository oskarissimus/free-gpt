output "cloud_function_url" {
  value       = google_cloudfunctions_function.chatgpt_scheduler.https_trigger_url
  description = "The URL to trigger the ChatGPT Cloud Function."
}
