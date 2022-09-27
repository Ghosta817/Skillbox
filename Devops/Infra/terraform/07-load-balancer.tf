resource "yandex_lb_network_load_balancer" "lb-ghost" {
  name = "lb-ghost"

  listener {
    name = "listener-prod"
    port = 8080
    external_address_spec {
      ip_version = "ipv4"
    }
  }

  attached_target_group {
    target_group_id = yandex_lb_target_group.prod-server.id

    healthcheck {
      name = "http-healthcheck"
      http_options {
        port = 8080
        path = "/"
      }
    }
  }
}

resource "yandex_lb_target_group" "prod-server" {
  name = "prod-target-group"

  dynamic "target" {
    for_each = (yandex_compute_instance.prod.*.network_interface.0.ip_address)
    content {
      subnet_id = yandex_vpc_subnet.subnet_terraform.id
      address   = target.value
    }

  }
}
