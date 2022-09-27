[test_srv]
${test_host} ansible_user=${test_user} ansible_ssh_private_key_file=${test_ssh}

[prod_srv]
${prod_host} ansible_user=${prod_user} ansible_ssh_private_key_file=${prod_ssh}

[monitor_srv]
${monitor_host} ansible_user=${monitor_user} ansible_ssh_private_key_file=${monitoring_ssh} int_monitor_ip=${monitor_inner_ip}

[log_srv]
${log_host} ansible_user=${log_user} ansible_ssh_private_key_file=${log_ssh} int_log_ip=${log_inner_ip}

[all:children]
test_srv
prod_srv
monitor_srv
log_srv

[app_srvs:children]
test_srv
prod_srv