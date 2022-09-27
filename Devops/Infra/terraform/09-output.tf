output "internal_ip_test_server" {
  value = yandex_compute_instance.test.network_interface.0.ip_address
}

output "internal_ip_monitoring_server" {
  value = yandex_compute_instance.monitoring.network_interface.0.ip_address
}

output "internal_ip_prod_server" {
  value = yandex_compute_instance.prod.network_interface.0.ip_address
}

output "internal_ip_log_server" {
  value = yandex_compute_instance.log.network_interface.0.ip_address
}

output "external_ip_test_server" {
  value = yandex_compute_instance.test.network_interface.0.nat_ip_address
}

output "external_ip_monitoring_server" {
  value = yandex_compute_instance.monitoring.network_interface.0.nat_ip_address
}

output "external_ip_prod_server" {
  value = yandex_compute_instance.prod.network_interface.0.nat_ip_address
}

output "external_ip_log_server" {
  value = yandex_compute_instance.log.network_interface.0.nat_ip_address
}

output "network_load_balancer_ip_address" {
  value = [for value in yandex_lb_network_load_balancer.lb-ghost.listener : value.external_address_spec.*][0][0].address
}

data "template_file" "inventory" {
  template    = file("./template/hosts.tpl")

  vars = {
    test_user = var.test-server-username
    test_ssh  = var.test-ssh-key-path
    test_host = join("", [yandex_compute_instance.test.name, " ansible_host=", yandex_compute_instance.test.network_interface.0.nat_ip_address])

    prod_user = var.prod-server-username
    prod_ssh  = var.prod-ssh-key-path
    prod_host = join("", [yandex_compute_instance.prod.name, " ansible_host=", yandex_compute_instance.prod.network_interface.0.nat_ip_address])

    monitor_user     = var.monitoring-server-username
    monitoring_ssh   = var.monitoring-ssh-key-path
    monitor_host     = join("", [yandex_compute_instance.monitoring.name, " ansible_host=", yandex_compute_instance.monitoring.network_interface.0.nat_ip_address])
    monitor_inner_ip = yandex_compute_instance.monitoring.network_interface.0.ip_address

    log_user     = var.log-server-username
    log_ssh      = var.log-ssh-key-path
    log_host     = join("", [yandex_compute_instance.log.name, " ansible_host=", yandex_compute_instance.log.network_interface.0.nat_ip_address])
    log_inner_ip = yandex_compute_instance.log.network_interface.0.ip_address

  }
}

resource "local_file" "save_inventory" {
  content  = data.template_file.inventory.rendered
  filename = "../ansible/hosts"
}
