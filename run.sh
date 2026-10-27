#!/usr/bin/env bash
set -euo pipefail; cd "$(dirname "$0")"; PORT=4329
if ss -ltn | grep -q "127.0.0.1:$PORT "; then echo "already serving http://127.0.0.1:$PORT/"; else
nohup python3 server.py > /tmp/family-sports-photo-desk-$PORT.log 2>&1 & sleep 1; echo "serving http://127.0.0.1:$PORT/ (pid $!)"; fi
