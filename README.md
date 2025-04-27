# Документация к сборке Xray с Traefik и WebSocket

## Содержание
1. [Описание проекта](#описание-проекта)
2. [Архитектура решения](#архитектура-решения)
3. [Конфигурация и основные компоненты](#конфигурация-и-основные-компоненты)
4. [Инструкция по установке](#инструкция-по-установке)
5. [Протоколы и точки входа](#протоколы-и-точки-входа)
6. [Мониторинг и статистика](#мониторинг-и-статистика)
7. [Добавление VLESS-REALITY на кастомном порту](#добавление-vless-reality-на-кастомном-порту)
8. [Управление клиентами](#управление-клиентами)
9. [Дополнительные утилиты](#дополнительные-утилиты)

## Описание проекта

Данный проект представляет собой готовое решение для развертывания Xray сервера с использованием Traefik в качестве обратного прокси и балансировщика нагрузки. Конфигурация включает в себя:

- Поддержку протоколов Shadowsocks и VLESS
- WebSocket транспорт для обхода блокировок
- Автоматическое получение и обновление SSL-сертификатов через Let's Encrypt
- Мониторинг с использованием Prometheus и Grafana
- Утилиты для получения URL-ссылок для клиентов

## Архитектура решения

## Конфигурация и основные компоненты

### Docker Compose

Файл `docker-compose.yml` определяет все сервисы и их конфигурацию. Основные сервисы:

- **traefik** - настройка прокси-сервера с TLS
- **nginx** - хостинг ссылок подписки
- **xray** - основной сервер прокси
- **v2ray-exporter** - экспортер метрик для Prometheus
- **prometheus** - сбор и хранение метрик
- **grafana** - визуализация метрик

### Конфигурация Xray

Файл `v2ray.json` содержит настройки Xray, включая:

- Inbounds - входящие соединения для разных протоколов и портов
- Outbounds - исходящие соединения
- Routing - правила маршрутизации трафика
- DNS - настройки DNS-серверов
- Policy - политики для соединений

## Инструкция по установке

1. Клонировать репозиторий:
   ```bash
   git clone <репозиторий> && cd xray_traefik
   ```

2. Скачать необходимые файлы геолокации:
   ```bash
   wget https://github.com/v2ray/geoip/releases/latest/download/geoip.dat -O geoip.dat && wget https://github.com/v2ray/domain-list-community/releases/latest/download/dlc.dat -O geosite.dat
   ```

3. Создать файлы конфигурации из образцов:
   ```bash
   cp .env.sample .env
   cp v2ray.json.sample v2ray.json
   ```

4. Отредактировать файлы конфигурации:
   - В `.env` указать ваш домен и email для Let's Encrypt
   - В `v2ray.json` настроить пароли, ID клиентов и другие параметры

5. Запустить сервисы:
   ```bash
   docker-compose up -d
   ```

## Протоколы и точки входа

Проект поддерживает следующие протоколы и точки входа:

### Shadowsocks
- Несколько портов (8000, 8080, 993, 40024, 8443, 8081)
- Метод шифрования: chacha20-ietf-poly1305

### VLESS с WebSocket
- Порт 8388 с путем `/ws`
- Порт 8389 с путем `/public_ws` (для публичного домена)
- Порт 8390 с путем `/friend_ws` (для друзей)
- Порт 8444 с путем `/vless_ws`

### VLESS с REALITY (подготовлен но закомментирован)
- Порт 8447 (закомментирован в docker-compose.yml)
- Защищён протоколом REALITY для дополнительной безопасности

## Мониторинг и статистика

Мониторинг осуществляется с помощью связки Prometheus и Grafana:

1. **v2ray-exporter** собирает метрики с Xray по адресу 127.0.0.1:10085
2. **Prometheus** получает данные от экспортера и хранит их
3. **Grafana** подключается к Prometheus и отображает данные в виде дашбордов

Доступ к Grafana осуществляется по URL `https://yourdomain.com/grafana` с логином `admin` и паролем `password` (по умолчанию).

Prometheus доступен по URL `https://yourdomain.com/prometheus` с базовой аутентификацией (логин: vpn).

## Добавление VLESS-REALITY на кастомном порту

Для добавления VLESS-REALITY на кастомном порту (например, 8443) выполните следующие шаги:

1. **Отредактируйте файл v2ray.json**, добавив новый inbound:
   ```json
   {
     "listen": "0.0.0.0",
     "port": 8443,
     "protocol": "vless",
     "settings": {
       "clients": [
         {
           "id": "ваш-уникальный-uuid",
           "level": 0,
           "email": "custom-reality@example.com",
           "flow": "xtls-rprx-vision"
         }
       ],
       "decryption": "none"
     },
     "streamSettings": {
       "network": "tcp",
       "security": "reality",
       "realitySettings": {
         "show": false,
         "dest": "www.microsoft.com:443",
         "serverNames": [
           "www.microsoft.com",
           "microsoft.com"
         ],
         "privateKey": "сгенерируйте-приватный-ключ",
         "shortIds": ["случайные-идентификаторы"],
         "publicKey": "соответствующий-публичный-ключ"
       }
     },
     "label": "Vpn | vless-reality-8443",
     "sniffing": {
       "enabled": true,
       "destOverride": ["http", "tls"]
     }
   }
   ```

2. **Сгенерируйте ключи Reality** с помощью команды:
   ```bash
   xray x25519
   ```
   И добавьте полученные ключи в конфигурацию.

3. **Добавьте соответствующую конфигурацию в docker-compose.yml**, раскомментировав или добавив:
   ```yaml
   # Reality connection 8443
   - "traefik.tcp.routers.v2ray-reality-8443.rule=HostSNI(`*`)"
   - "traefik.tcp.routers.v2ray-reality-8443.entrypoints=reality8443"
   - "traefik.tcp.routers.v2ray-reality-8443.service=v2ray-reality-8443"
   - "traefik.tcp.services.v2ray-reality-8443.loadbalancer.server.port=8443"
   ```

4. **Добавьте новую точку входа в Traefik** в секции command:
   ```yaml
   - "--entrypoints.reality8443.address=:8443"
   ```

5. **Перезапустите контейнеры**:
   ```bash
   docker-compose down && docker-compose up -d
   ```

6. **Проверьте работу** нового протокола через скрипт `clients.py`.

## Управление клиентами

Для управления клиентами используется скрипт `clients.py`, который:
- Читает конфигурацию из `v2ray.json`
- Генерирует URL для подключения по Shadowsocks и VLESS
- Выводит их в удобном формате

Для получения ссылок выполните:
```bash
python3 clients.py
```

## Дополнительные утилиты

1. **encode_ss.py** - скрипт для кодирования Shadowsocks URL
   ```bash
   python3 encode_ss.py <Метод шифрования> <Пароль> <Сервер> <Порт>
   ```

2. **decode_ss.py** - скрипт для декодирования Shadowsocks URL
   ```bash
   python3 decode_ss.py <Shadowsocks URL>
   ```

3. **Prometheus и Grafana** - для мониторинга производительности и использования:
   - Prometheus: `https://<domain>/prometheus`
   - Grafana: `https://<domain>/grafana` 