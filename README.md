# simple start
1. clone repo
2. `wget https://github.com/v2ray/geoip/releases/latest/download/geoip.dat -O geoip.dat && wget https://github.com/v2ray/domain-list-community/releases/latest/download/dlc.dat -O geosite.dat`
3. `mv .env.sample .env` and `mv v2ray.json.sample v2ray.json`
4. configure .env and v2ray.json
5. docker-compose up -d

clients.py - print URL ss:// and vless://



# Запуск

1. Склонируйте репозиторий и отредактируйте файл .env добавив валидный домен и эмейл.
2. Скачайте geoip ```wget https://github.com/v2ray/geoip/releases/latest/download/geoip.dat -O geoip.dat && wget https://github.com/v2ray/domain-list-community/releases/latest/download/dlc.dat -O geosite.dat```
3. Отредактируйте v2ray.json. Данный пример рассчитан на использование websocket vless, хотя сейчас рекомендуется использовать reality подключение. Эти соединения не могут оба быть на 443 порту. Поэтому, если вы хотите использовать reality подключение, раскоменнтируйте в `docker-compose.yaml` лейблы у `# Reality connection` и закомментируйте все `WebSocket connection`
