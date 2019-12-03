#!/usr/bin/env python3

import time
import random
import subprocess
import json
from pathlib import Path
import sys

if len(sys.argv) - 1 == 1:
    if sys.argv[1] == "start":
        data = json.loads(subprocess.run(["alfred-json", "-r 64"], capture_output=True).stdout)
        discovery_node = None

        for key, value in data.items():
            if value['discovery']:
                print("Found discovery node: %%", value['hostname'])
                discovery_node = value['ipaddr']
                break

        if discovery_node is None:
            print("No discovery node found. Waiting...")
            time.sleep(1)
            time.sleep(random.randrange(1,1000)/10)
            data = json.loads(subprocess.run(["alfred-json", "-r 64"], capture_output=True).stdout)
            for key, value in data.items():
                if value['discovery']:
                    print("Found discovery node: %%", value['hostname'])
                    discovery_node = value['ipaddr']
                    break
            if discovery_node is None:
                print("No discovery node found. I am the new one!")
                Path('/run/discovery').touch()
                subprocess.run(["systemctl", "start", "update-alfred.service"])
                discovery_node = "self"

        subprocess.run(["vernemq", "start"])

        if discovery_node != "self":
            print("Joining the cluster with discovery node %%", discovery_node)
            subprocess.run(["vmq-admin", "cluster", "join", "discovery-node=vernemq@" + discovery_node])
    if sys.argv[1] == "stop":
        print("Leaving cluster")
        subprocess.run(["vmq-admin", "cluster", "leave", "node=vernemq@" + ni.ifaddresses('bat0')[2][0]['addr'], "-k"])
        print("Stopping vernemq")
        subprocess.run(["vernemq", "stop"])