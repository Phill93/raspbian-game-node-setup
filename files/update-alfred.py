#!/usr/bin/env python3

import socket
import netifaces as ni
import json
import subprocess

hostname = socket.gethostname()
ip = ni.ifaddresses('bat0')[2][0]['addr']

if 'eth0' in ni.interfaces():
    role = "border"
else:
    role = "inner"

data = {
    'hostname': hostname,
    'ipaddr': ip,
    'role': role
}

process = subprocess.Popen(["alfred", "-s 64"], stdin=subprocess.PIPE)

process.stdin.write(json.dumps(data).encode())
process.stdin.close()