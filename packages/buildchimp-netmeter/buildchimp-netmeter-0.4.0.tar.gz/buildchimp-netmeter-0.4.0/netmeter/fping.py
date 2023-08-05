import subprocess
import re
import time
from netmeter.config import (TARGETS, COUNT)

FPING_LINE_RE = "\s*[:,=\/]%?\s*"
DEFAULT_COUNT = 20
DEFAULT_TARGETS = ['8.8.8.8']

def fping(sender, prefix, config):
    ping_count = config.get(COUNT) or DEFAULT_COUNT
    command=['/usr/sbin/fping', '-c', str(ping_count), '-q']
    command.extend(config[TARGETS] or DEFAULT_TARGETS)

    records = {}

    print(f"Running '{command}'")
    process = subprocess.Popen(command, stderr=subprocess.PIPE)
    out = process.communicate()[1].decode('utf-8')
    # print(f"Got output:\n{out}\n")

    for line in out.splitlines():
        # line = process.stdout.readline()
        # print(f"Line: '{line}'")
        if line == '':
            continue

        # Sample output:
        # 8.8.8.8     : xmt/rcv/%loss = 5/5/0%, min/avg/max = 75.3/79.5/89.7
        # www.cnn.com : xmt/rcv/%loss = 5/5/0%, min/avg/max = 43.3/46.8/49.5
        #  
        # re.split(FPING_LINE_RE, line) splits into:
        # ['8.8.8.8', 'xmt', 'rcv', '%loss', '5', '5', '0%', 'min', 'avg', 'max', '75.3', '79.5', '89.7']
        #  
        # print(f"Processing output line: '{line}'")
        outer = re.split(FPING_LINE_RE, line.rstrip())
        basename = f"{prefix}.fping.{outer[0].replace('.', '_')}"

        now = int(time.time())

        # print(f"Split line: {outer}")
        if len(outer) > 9:
            for n in range(1,4):
                key = f"{basename}.{outer[n]}"
                val = outer[n+3]
                if val.endswith('%'):
                    val = val[:-1]

                print(f"Added: {key} = {val}")
                sender.send_raw(f"{key} {val} {now}")

            for n in range(7,10):
                key = f"{basename}.{outer[n]}"
                val = outer[n+3]

                print(f"Added: {key} = {val}")
                sender.send_raw(f"{key} {val} {now}")
