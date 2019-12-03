#!/usr/bin/env python3

import socket
import netifaces as ni
import json
import os

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

os.system('alfred -s 64 ' + json.dumps(data))