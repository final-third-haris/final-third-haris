#!/bin/bash
cd "$(dirname "$0")"
echo "Starting Final Third local server..."
python3 -m http.server 8080 &
SERVER_PID=$!
sleep 1
open "http://localhost:8080"
echo "======================================================="
echo "FINAL THIRD is running at: http://localhost:8080"
echo "YouTube video playback is active and enabled."
echo "Close this Terminal window when you are done."
echo "======================================================="
wait $SERVER_PID
