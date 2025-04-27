# Xray с Traefik и WebSocket

Готовое решение для развертывания Xray-сервера с Traefik в качестве обратного прокси.

**О статусе проекта:**
Хотя решение функционально, оно имеет ограничения:
- Множество открытых портов создаёт потенциальные уязвимости
- Поддержка подписок только для v2rayng
- Отсутствие удобного управления пользователями

Для расширенных возможностей рекомендуется Remnawavе с улучшенным интерфейсом и управлением.

**Возможности:**
- Протоколы Shadowsocks и VLESS
- WebSocket транспорт
- Автоматические SSL-сертификаты через Let's Encrypt
- Мониторинг (Prometheus, Grafana)
- Генерация URL для клиентов

## Быстрый старт

1. Клонировать и подготовить:
   ```bash
   git clone <репозиторий> && cd xray_traefik
   wget https://github.com/v2ray/geoip/releases/latest/download/geoip.dat -O geoip.dat && wget https://github.com/v2ray/domain-list-community/releases/latest/download/dlc.dat -O geosite.dat
   cp .env.sample .env && cp v2ray.json.sample v2ray.json
   ```

2. Настроить:
   - В `.env`: ваш домен и email
   - В `v2ray.json`: пароли и ID клиентов

3. Запустить:
   ```bash
   docker-compose up -d
   ```

## Поддерживаемые протоколы

### Shadowsocks
- Порты: 8000, 8080, 993, 40024, 8443, 8081
- Шифрование: chacha20-ietf-poly1305

### VLESS WebSocket
- 8388: `/ws`
- 8389: `/public_ws`
- 8390: `/friend_ws`
- 8444: `/vless_ws`


## Управление и утилиты

- **clients.py**: генерация URL-ссылок (`python3 clients.py`)
- **encode_ss.py/decode_ss.py**: работа с Shadowsocks URL
- **Мониторинг**:
  - Prometheus: `https://<domain>/prometheus` (логин: vpn)
  - Grafana: `https://<domain>/grafana` (логин: admin, пароль: password) 