resource "google_secret_manager_secret" "email_username" {
  secret_id = "email_username"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "email_username" {
  secret      = google_secret_manager_secret.email_username.id
  secret_data = var.email_username
}

resource "google_secret_manager_secret" "email_password" {
  secret_id = "email_password"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "email_password" {
  secret      = google_secret_manager_secret.email_password.id
  secret_data = var.email_password
}
