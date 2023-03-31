
resource "google_compute_instance" "executor_instance" {
  name                      = "executor-instance"
  machine_type              = "e2-standard-4"
  zone                      = var.zone
  deletion_protection       = false
  allow_stopping_for_update = true
  desired_status            = var.vm_status
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

