#cloud-config
ssh_pwauth: no
users:
  - name: ${monitoring_user}
    groups: sudo
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh_authorized_keys:
      - ${ssh_key_skillbox_monitor}
