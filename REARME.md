# V2Ray with Traefik

This repository sets up V2Ray with Traefik as a reverse proxy, allowing multiple WebSocket and Shadowsocks connections with automatic SSL management via Let's Encrypt.

## Features

- **Traefik Reverse Proxy:** Manages SSL termination and routing.
- **V2Ray Configuration:** Supports multiple inbound connections.
- **Dynamic Routing:** Based on hostnames and paths.

## Prerequisites

- Docker
- Docker Compose

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/momai/v2ray_traefik.git
   cd v2ray_traefik
```
2. **Update Configuration:**

- Edit `docker-compose.yml`: Update domain names in the Traefik labels.
```
traefik.http.routers.v2ray-ws1.rule=Host(`vpn.momai.dev`) && PathPrefix(`/ws`)
```
- Edit v2ray.json: Add additional servers in the inbounds array.
```
{
  "listen": "0.0.0.0",
  "port": 8391,
  "protocol": "shadowsocks",
  "settings": {
    "password": "your_password_here",
    "method": "chacha20-ietf-poly1305"
  },
  "server_name": "vpn.momai.dev"
}```
3. **Start Services:**
`docker-compose up -d`

## Python Scripts
- generate_v2ray_config.py: Generates V2Ray config entries.
```
python3 generate_v2ray_config.py --domain yourdomain.com --password yourpassword --port 8388
```
- update_traefik_config.py: Updates Traefik routing rules.
```
python3 update_traefik_config.py --domain yourdomain.com --path /newpath --port 8391
```

## Troubleshooting
- Logs: Use docker-compose logs traefik and docker-compose logs v2ray.
- Check Configuration: Ensure domains and paths are correct.
