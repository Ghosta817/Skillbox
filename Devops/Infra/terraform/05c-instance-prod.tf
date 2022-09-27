data "template_file" "prod_user" {
  template = file(var.prod-server-user-template)
  vars = {
    prod_user             = var.prod-server-username
    ssh_key_skillbox_prod = file(join("", [var.prod-ssh-key-path, ".pub"]))
  }
}

resource "yandex_compute_instance" "prod" {
  name        = var.prod-server-name
  hostname    = var.prod-server-name
  description = "Production server"

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
    user-data = data.template_file.prod_user.rendered
  }
}

