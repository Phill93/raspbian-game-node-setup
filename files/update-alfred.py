#!/usr/bin/env python3

import socket
import netifaces as ni
import json
import subprocess
import os
import time

hostname = socket.gethostname()
ip = ni.ifaddresses('bat0')[2][0]['addr']

if 'eth0' in ni.interfaces():
    role = "border"
else:
    role = "inner"

if os.path.exists("/run/discovery"):
    discovery = True
else:
    discovery = False

model = open("/sys/firmware/devicetree/base/model").read()

data = {
    'hostname': hostname,
    'ipaddr': ip,
    'role': role,
    'discovery': discovery,
    'model': model,
    'time': time.time()
}

process = subprocess.Popen(["alfred", "-s 64"], stdin=subprocess.PIPE, encoding='utf-8')

process.stdin.write(json.dumps(data))
process.stdin.close()