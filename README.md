# Xray with Traefik and WebSocket 

Ready-to-deploy solution for Xray server with Traefik as reverse proxy.

**Project status:** While this solution remains functional, it has some limitations:

* Multiple open ports create potential security vulnerabilities
* Subscription support limited to v2rayng
* Lack of convenient user management

For extended capabilities, consider Remnawavе with its improved interface and management features.

**Features:**

* Shadowsocks and VLESS protocols
* WebSocket transport
* Automatic SSL certificates via Let's Encrypt
* Monitoring (Prometheus, Grafana)
* Client URL generation

### Quick Start

1. Clone and prepare:
   ```bash
   git clone <repository> && cd xray_traefik
   wget https://github.com/v2ray/geoip/releases/latest/download/geoip.dat -O geoip.dat && wget https://github.com/v2ray/domain-list-community/releases/latest/download/dlc.dat -O geosite.dat
   cp .env.sample .env && cp v2ray.json.sample v2ray.json
   ```

2. Configure:
   - In `.env`: your domain and email
   - In `v2ray.json`: passwords and client IDs

3. Launch:
   ```bash
   docker-compose up -d
   ```

### Supported Protocols

**Shadowsocks**
- Ports: 8000, 8080, 993, 40024, 8443, 8081
- Encryption: chacha20-ietf-poly1305

**VLESS WebSocket**
- 8388: `/ws`
- 8389: `/public_ws`
- 8390: `/friend_ws`
- 8444: `/vless_ws`

### Management and Utilities

- **clients.py**: URL generation (`python3 clients.py`)
- **encode_ss.py/decode_ss.py**: Shadowsocks URL handling
- **Monitoring**:
  - Prometheus: `https://<domain>/prometheus` (login: vpn)
  - Grafana: `https://<domain>/grafana` (login: admin, password: password)

