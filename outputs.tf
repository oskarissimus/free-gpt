output "cloud_function_url" {
  value       = google_cloudfunctions_function.chatgpt_scheduler.https_trigger_url
  description = "The URL to trigger the ChatGPT Cloud Function."
}

output "executor_instance_ip" {
  value       = google_compute_instance.executor_instance.network_interface.0.access_config.0.nat_ip
  description = "The IP address of the executor instance."
}
 
