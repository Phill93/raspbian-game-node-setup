#!/usr/bin/env python3

import socket
import netifaces as ni
import json
from subprocess import check_output

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

check_output(["alfred", "-s 64"], stdin=json.dumps(data))