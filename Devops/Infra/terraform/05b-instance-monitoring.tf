data "template_file" "monitoring_user" {
  template = file(var.monitoring-server-user-template)
  vars = {
    monitoring_user          = var.monitoring-server-username
    ssh_key_skillbox_monitor = file(join("", [var.monitoring-ssh-key-path, ".pub"]))
  }
}

resource "yandex_compute_instance" "monitoring" {
  name        = var.monitoring-server-name
  hostname    = var.monitoring-server-name
  description = "Server for monitoring"

  platform_id               = var.instance-platform-id
  allow_stopping_for_update = true

  resources {
    cores         = var.instance-cores
    memory        = var.instance-memory
    core_fraction = var.instance-core-fraction
  }

  boot_disk {
    initialize_params {
      image_id = var.instance-image-id
      type     = var.instance-disk-type
      size     = var.instance-disk-size
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet_terraform.id
    nat       = true
  }

  scheduling_policy {
    preemptible = var.is-auto-shutdown
  }

  metadata = {
    user-data = data.template_file.monitoring_user.rendered
  }
}