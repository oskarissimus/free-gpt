resource "google_secret_manager_secret" "gmail_username" {
  secret_id = "gmail_username"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "gmail_username" {
  secret      = google_secret_manager_secret.gmail_username.id
  secret_data = var.gmail_username
}

resource "google_secret_manager_secret" "gmail_password" {
  secret_id = "gmail_password"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "gmail_password" {
  secret      = google_secret_manager_secret.gmail_password.id
  secret_data = var.gmail_password
}
