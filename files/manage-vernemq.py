#!/usr/bin/env python3

import time
import random
import subprocess
import json
from pathlib import Path

data = json.loads(subprocess.run(["alfred-json", "-r 64"], capture_output=True).stdout)

for node in data:
    if node['discovery']:
        discovery_node = node['ipaddr']
        break

if not discovery_node:
    time.sleep(1)
    time.sleep(random.randrange(1,1000)/10)
    for node in data:
        if node['discovery']:
            discovery_node = node['ipaddr']
            break
    if not discovery_node:
        Path('/run/discovery').touch()
        subprocess.run(["systemctl", "start", "update-alfred.service"])
        discovery_node = "self"

subprocess.run(["vernemq", "start"])

if discovery_node != "self":
    subprocess.run(["vmp-admin", "cluster", "join", "discovery-node=vernemq@" + discovery_node])