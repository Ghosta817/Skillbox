resource "yandex_vpc_network" "network_terraform" {
  name = "network_terraform"
}

resource "yandex_vpc_subnet" "subnet_terraform" {
  name           = "subnet_terraform"
  network_id     = yandex_vpc_network.network_terraform.id
  v4_cidr_blocks = ["10.10.0.0/24"]
}
