## Инфраструктура для тестирования.


### Раздел Infrastructure.

В папке ansible находится код для установки  Docker, Gitlab-runner на тестовый сервер, а так же Prometheus и Grafana на мониторинг сервер.
В папке terraform лежит код для резвертывания тестового и мониторинг серверов.  
Для работы требуются установелнный Ansible, Terraform, действующий аккаунт в Yandex Cloud и доступ в данный gitlab репозиторий.


### Установка

0. Склонировать репозиторий к себе командой: 
    ```bash
    $ git clone git@gitlab.skillbox.ru:ilia_k/infra.git
    ```   
    Далее переходим в папку "*infra/4/*"

1. Для работы Terraform нужны:  
    1.1 VPN для первоначальной инициализации Terraform (либо варинат от Yandex Cloud)  
    1.2 Заполненый **terraform.tfvars.example** файл и переименованный в **terraform.tfvars**  
    1.3 Все найстройки и переменные находятся в **00-vars.tf**  
    1.4 Проверить наличие и путь к SSH ключам в **00-vars.tf**  

2. Ansible   
    2.0 Для работы плейбука необходима установка следующих модулей:
    ```bash
    $ ansible-galaxy collection install community.grafana
    ```
    2.1 Файл hosts для Ansible генерируется с помощью Terraform после успешного развертывания инфраструктуры.  
    2.2 Установка всего ПО осуществляется командой:
    ```bash
    $ ansible-playbook playbook.yml
    ```  
    либо с использованием тегов.