resource "yandex_dns_zone" "zone1" {
  name        = "my-public-zone"
  description = "Test public zone"

  labels = {
    label1 = "skillbox_diploma.domain"
  }

  zone   = var.domain-name
  public = true
}

resource "yandex_dns_recordset" "rs1" {
  zone_id = yandex_dns_zone.zone1.id
  name    = var.domain-name
  type    = "A"
  ttl     = 200
  data    = [[for value in yandex_lb_network_load_balancer.lb-ghost.listener : value.external_address_spec.*][0][0].address]
}

resource "yandex_dns_recordset" "rs2" {
  zone_id = yandex_dns_zone.zone1.id
  name    = join(".", [var.domain-name-prefix-prometheus, var.domain-name])
  type    = "A"
  ttl     = 200
  data    = [yandex_compute_instance.monitoring.network_interface.0.nat_ip_address]
}

resource "yandex_dns_recordset" "rs3" {
  zone_id = yandex_dns_zone.zone1.id
  name    = "${var.domain-name-prefix-grafana}.${var.domain-name}"
  type    = "CNAME"
  ttl     = 200
  data    = [yandex_dns_recordset.rs2.name]
}

resource "yandex_dns_recordset" "rs4" {
  zone_id = yandex_dns_zone.zone1.id
  name    = var.domain-name-prefix-test
  type    = "A"
  ttl     = 200
  data    = [yandex_compute_instance.test.network_interface.0.nat_ip_address]
}