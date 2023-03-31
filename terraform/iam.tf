resource "google_project_service" "cloudfunctions" {
  project = var.project_id
  service = "cloudfunctions.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}

resource "google_project_service" "cloudbuild" {
  project = var.project_id
  service = "cloudbuild.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}

resource "google_project_service" "cloudscheduler" {
  project = var.project_id
  service = "cloudscheduler.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false

}

resource "google_project_service" "compute" {
  project = var.project_id
  service = "compute.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false

}

resource "google_project_service" "bigquery" {
  project = var.project_id
  service = "bigquery.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}

resource "google_project_service" "secretmanager" {
  project = var.project_id
  service = "secretmanager.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}
resource "google_project_iam_member" "cloudbuild_storage_object_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${data.google_project.current.number}@cloudbuild.gserviceaccount.com"
}

resource "time_sleep" "wait_for_services" {
  depends_on = [
    google_project_service.cloudfunctions,
    google_project_service.cloudbuild,
    google_project_service.cloudscheduler,
    google_project_service.compute,
    google_project_service.bigquery,
    google_project_service.secretmanager,
  ]
  create_duration = "5m"
}


resource "google_project_iam_custom_role" "secrets_viewer" {
  role_id     = "secretsViewer"
  title       = "Secrets Viewer"
  description = "View secrets in the project"
  project     = var.project_id

  permissions = [
    "secretmanager.secrets.get",
    "secretmanager.versions.get",
    "secretmanager.versions.access",
  ]
}

resource "google_service_account" "vm_instance_service_account" {
  account_id   = "vm-instance-service-account"
  display_name = "VM Instance Service Account"
}

resource "google_project_iam_member" "vm_instance_secrets_viewer" {
  project = var.project_id
  role    = google_project_iam_custom_role.secrets_viewer.id
  member  = "serviceAccount:${google_service_account.vm_instance_service_account.email}"
}

