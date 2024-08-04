#!/usr/bin/python3

import base64
import sys
from urllib.parse import urlparse

def decode_shadowsocks_url(url):
    # Разбор URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme == 'ss':
        raise ValueError("Неправильный формат URL. Убедитесь, что URL начинается с 'ss://'.")

    # Получение закодированной части из URL
    encoded_security = parsed_url.netloc.split('@')[0]

    # Раскодирование информации о методе шифрования и пароле
    decoded_security = base64.b64decode(encoded_security).decode('ascii')
    method, password = decoded_security.split(':', 1)

    # Вывод информации
    print(f"Метод шифрования: {method}")
    print(f"Пароль: {password}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python3 decode_ss.py <Shadowsocks URL>")
        sys.exit(1)

    ss_url = sys.argv[1]
    try:
        decode_shadowsocks_url(ss_url)
    except Exception as e:
        print(f"Ошибка: {e}")
