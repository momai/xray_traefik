#!/usr/bin/python3

import base64
import json
import sys
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

# Function to load JSON without comments
def load_json_without_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Remove lines that start with '#'
    json_str = ''.join(line for line in lines if not line.strip().startswith('#'))
    return json.loads(json_str)

path = Path(__file__).parent
config_path = path.joinpath('v2ray.json')

try:
    config = load_json_without_comments(str(config_path))
except json.JSONDecodeError as e:
    print(f"Error loading JSON: {e}")
    sys.exit(1)

# Attempt to get the public IP address
try:
    ip = urlopen("https://ipv4.icanhazip.com/").read().decode().rstrip()
except Exception as e:
    print(f"Error getting IP: {e}")
    sys.exit(1)

# Print header once
print("\033[1m\033[34mShadowsocks:\033[0m")

# Generate Shadowsocks URL for each inbound
for inbound in config.get('inbounds', []):
    if inbound.get('protocol') == 'shadowsocks':
        port = str(inbound.get('port'))
        method = inbound.get('settings', {}).get('method')
        password = inbound.get('settings', {}).get('password')
        server_name = inbound.get('server_name', ip)
        label = inbound.get('label', 'Unnamed-Server')

        if method and password:
            # Encode method and password for Shadowsocks
            security = base64.b64encode(f"{method}:{password}".encode('ascii')).decode('ascii')
            # Encode label for URL
            encoded_label = quote(label)
            
            # Check for WebSocket settings
            stream_settings = inbound.get('streamSettings', {})
            if stream_settings.get('network') == 'ws':
                ws_path = stream_settings.get('wsSettings', {}).get('path', '')
                plugin_options = f"v2ray-plugin;path={ws_path};tls"
                ss_url = f"ss://{security}@{server_name}:{port}?plugin={quote(plugin_options)}#{encoded_label}"
            else:
                # Create regular Shadowsocks URL
                ss_url = f"ss://{security}@{server_name}:{port}#{encoded_label}"

            # Print server name and URL
            print(f"{label}")
            print(f"{ss_url}\n")
        else:
            print("Error: Method or password missing for Shadowsocks.")

# Print header for VLESS
print("\033[1m\033[34mVLESS:\033[0m")

# Generate VLESS URL for each inbound
for inbound in config.get('inbounds', []):
    if inbound.get('protocol') == 'vless':
        # Use port 443 for VLESS connections
        port = '443'
        clients = inbound.get('settings', {}).get('clients', [])
        server_name = inbound.get('server_name', ip)
        label = inbound.get('label', 'Unnamed-Server')

        for client in clients:
            uuid = client.get('id')
            email = client.get('email', 'Unnamed-Client')
            encoded_label = quote(f"{label} ({email})")

            stream_settings = inbound.get('streamSettings', {})
            network = stream_settings.get('network', 'tcp')
            ws_path = stream_settings.get('wsSettings', {}).get('path', '')

            vless_url = f"vless://{uuid}@{server_name}:{port}?encryption=none&type={network}&path={quote(ws_path)}&security=tls#{encoded_label}"

            # Print VLESS URL
            print(f"{label} ({email})")
            print(f"{vless_url}\n")
