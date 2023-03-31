variable "project_id" {
  description = "The project ID to deploy the resources in."
}

variable "region" {
  description = "The region to deploy the resources in."
}

variable "zone" {
  description = "The zone to deploy the resources in."
}

variable "openai_api_key" {
  description = "The API key for ChatGPT."
}

variable "instance_username" {
  description = "The username for the executor instance."
}

variable "email_username" {
  description = "The username for the email account."
}

variable "email_password" {
  description = "The password for the email account."
}

variable "vm_status" {
  description = "The desired status of the executor instance."
}

variable "scheduler_paused" {
  description = "Whether the scheduler should be paused."
}
