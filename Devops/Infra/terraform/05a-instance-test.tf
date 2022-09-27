data "template_file" "test_user" {
  template = file(var.test-server-user-template)
  vars = {
    test_user        = var.test-server-username
    ssh_key_skillbox = file(join("", [var.test-ssh-key-path, ".pub"]))
  }
}

resource "yandex_compute_instance" "test" {
  name        = var.test-server-name
  hostname    = var.test-server-name
  description = "Server for tests"

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
    user-data = data.template_file.test_user.rendered
  }
}

# resource "local_file" "save_file" {
#   content  = data.template_file.test_user.rendered
#   filename = "./test_user"
# }
