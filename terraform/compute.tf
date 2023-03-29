
resource "google_compute_instance" "executor_instance" {
  name                = "executor-instance"
  machine_type        = "f1-micro"
  zone                = var.zone
  deletion_protection = false
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

