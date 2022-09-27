#============================= Yandex Cloud variables ==============================#

variable "zone" {
  description = "Deafult zone"
  default     = "ru-central1-a"
}

variable "yandex-token" {
  description = "Yandex token"
}

variable "yandex-cloud-id" {
  description = "Yandex cloud id"
}

variable "yandex-folder-id" {
  description = "Yandex folder id"
}

variable "yandex-service-account-id" {
  description = "Yandex service account id"
}

#================================ DNS variables ===================================#

variable "domain-name" {
  description = "Domain name"
  type        = string
  default     = "skillboxdevopsdiploma-ilya.gq."
}

variable "domain-name-prefix-test" {
  description = "Prefix for test servers"
  type        = string
  default     = "test"
}

variable "domain-name-prefix-prometheus" {
  description = "Prefix for prometheus"
  type        = string
  default     = "monitoring"
}

variable "domain-name-prefix-grafana" {
  description = "Prefix for grafana"
  type        = string
  default     = "grafana"
}

#=============================== Instance variables ==================================#

variable "instance-platform-id" {
  description = "Type of instance CPUs"
  type        = string
  default     = "standard-v3"
}

variable "instance-cores" {
  description = "Amount of CPU cores"
  type        = number
  default     = 2
}

variable "instance-memory" {
  description = "Amount of memory, GB"
  type        = number
  default     = 1
}

variable "instance-core-fraction" {
  description = "Fraction per core, %"
  type        = number
  default     = 20
}

variable "instance-image-id" {
  description = "Image for instances, Ubuntu 20.04 LTS"
  type        = string
  default     = "fd8anitv6eua45627i0e"
}

variable "instance-disk-type" {
  description = "Type of disk"
  type        = string
  default     = "network-hdd"
}

variable "instance-disk-size" {
  description = "Size of disk, GB"
  type        = number
  default     = 10
}

variable "is-auto-shutdown" {
  description = "Is 24h autoshutdown true"
  type        = bool
  default     = true
}

#=============================== Instances variables ==================================#


#--------------------- Test server ---------------------#

variable "test-server-username" {
  description = "Test instance user name"
  type        = string
  default     = "ghost_t"
}

variable "test-ssh-key-path" {
  description = "Test instance ssh public key path"
  type        = string
  default     = "~/.ssh/skillbox"
}

variable "yandex-test-instances" {
  description = "Amount of servers to start"
  default     = 1
}

variable "test-server-name" {
  description = "Name of test instance"
  type        = string
  default     = "test-server"
}

# variable "test-server-port" {
#   description = "Test server port for sub domain name"
#   type        = number
#   default     = 8080
# }

variable "test-server-user-template" {
  description = "Creat new user on each instance"
  default     = "./template/test_user.tpl"
}

#------------------ Monitoring server ------------------#

variable "monitoring-server-username" {
  description = "Monitoring instance user name"
  type        = string
  default     = "ghost_m"
}

variable "monitoring-ssh-key-path" {
  description = "Monitoring instance ssh public key path"
  type        = string
  default     = "~/.ssh/skillbox_monitor"
}

variable "monitoring-server-name" {
  description = "Name of monitoring instance"
  type        = string
  default     = "monitor-server"
}

# variable "monitoring-server-port" {
#   description = "Monitoring server port for sub domain name"
#   type        = number
#   default     = 9090
# }

# variable "grafana-server-port" {
#   description = "Grafana server port for sub domain name"
#   type        = number
#   default     = 3000
# }

variable "monitoring-server-user-template" {
  description = "Creat new user for monitoring instance"
  default     = "./template/monitoring_user.tpl"
}


#--------------------- Production server ---------------------#

variable "prod-server-username" {
  description = "Production instance user name"
  type        = string
  default     = "ghost_p"
}

variable "prod-ssh-key-path" {
  description = "Production instance ssh public key path"
  type        = string
  default     = "~/.ssh/skillbox_prod"
}

variable "yandex-prod-instances" {
  description = "Amount of servers to start"
  default     = 1
}

variable "prod-server-name" {
  description = "Name of production instance"
  type        = string
  default     = "prod-server"
}

# variable "prod-server-port" {
#   description = "Production server port for sub domain name"
#   type        = number
#   default     = 8080
# }

variable "prod-server-user-template" {
  description = "Creat new user on each instance"
  default     = "./template/prod_user.tpl"
}


#--------------------- Logs server ---------------------#

variable "log-server-username" {
  description = "Logs instance user name"
  type        = string
  default     = "ghost_l"
}

variable "log-ssh-key-path" {
  description = "Logs instance ssh public key path"
  type        = string
  default     = "~/.ssh/skillbox_log"
}

variable "yandex-log-instances" {
  description = "Amount of servers to start"
  default     = 1
}

variable "log-server-name" {
  description = "Name of logs instance"
  type        = string
  default     = "log-server"
}

variable "log-server-user-template" {
  description = "Creat new user on each instance"
  default     = "./template/log_user.tpl"
}
