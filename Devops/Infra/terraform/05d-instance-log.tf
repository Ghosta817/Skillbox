data "template_file" "log_user" {
  template = file(var.log-server-user-template)
  vars = {
    log_user             = var.log-server-username
    ssh_key_skillbox_log = file(join("", [var.log-ssh-key-path, ".pub"]))
  }
}

resource "yandex_compute_instance" "log" {
  name        = var.log-server-name
  hostname    = var.log-server-name
  description = "Logs server"

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
    user-data = data.template_file.log_user.rendered
  }
}

