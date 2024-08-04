#!/usr/bin/python3

import base64
import sys

def encode_shadowsocks_url(method, password, server, port):
    # Кодирование информации о методе шифрования и пароле
    security_info = f"{method}:{password}"
    encoded_security = base64.b64encode(security_info.encode('ascii')).decode('ascii')

    # Формирование полной Shadowsocks URL
    ss_url = f"ss://{encoded_security}@{server}:{port}"
    
    return ss_url

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Использование: python3 encode_ss.py <Метод шифрования> <Пароль> <Сервер> <Порт>")
        sys.exit(1)

    method = sys.argv[1]
    password = sys.argv[2]
    server = sys.argv[3]
    port = sys.argv[4]

    try:
        ss_url = encode_shadowsocks_url(method, password, server, port)
        print(f"Shadowsocks URL: {ss_url}")
    except Exception as e:
        print(f"Ошибка: {e}")
