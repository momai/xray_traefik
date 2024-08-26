1. clone repo
2. `wget https://github.com/v2ray/geoip/releases/latest/download/geoip.dat -O geoip.dat && wget https://github.com/v2ray/domain-list-community/releases/latest/download/dlc.dat -O geosite.dat`
3. `mv .env.sample .env` and `mv v2ray.json.sample v2ray.json`
4. configure .env and v2ray.json
5. docker-compose up -d

clients.py - print URL ss:// and vless://
