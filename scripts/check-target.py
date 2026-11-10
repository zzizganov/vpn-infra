#!/usr/bin/env python3
import socket
import ssl
import sys
name = sys.argv[1]
context = ssl.create_default_context()
context.minimum_version = ssl.TLSVersion.TLSv1_3
context.set_alpn_protocols(['h2'])
with socket.create_connection((name, 443), timeout=15) as sock:
    with context.wrap_socket(sock, server_hostname=name) as tls:
        assert tls.version() == 'TLSv1.3' and tls.selected_alpn_protocol() == 'h2'
print('TLS 1.3, H2 and hostname certificate verified')
