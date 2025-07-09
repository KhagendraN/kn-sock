#!/bin/bash

# test_kn_sock_all.sh - Full test suite for kn-sock CLI

PORT=8080
TMP_DIR="./kn_sock_test_dir"
TEST_FILE="./test_file.txt"
RECEIVED_FILE="$TMP_DIR/$(basename "$TEST_FILE")"

# Create test directory and test file
mkdir -p "$TMP_DIR"
echo "This is a test file." > "$TEST_FILE"

# Function to clean up background processes and files
cleanup() {
  echo "[*] Cleaning up..."
  pkill -f "kn-sock run-tcp-server" &> /dev/null
  pkill -f "kn-sock run-udp-server" &> /dev/null
  pkill -f "kn-sock run-file-server" &> /dev/null
  rm -rf "$TMP_DIR" "$TEST_FILE"
  echo "[*] Done."
}

# Exit handler
trap cleanup EXIT

echo "[*] Starting TCP server..."
kn-sock run-tcp-server "$PORT" &
TCP_PID=$!
sleep 1

echo "[*] Sending TCP message..."
kn-sock send-tcp localhost "$PORT" "Hello from TCP test"

sleep 1
kill $TCP_PID

echo "[*] Starting UDP server..."
kn-sock run-udp-server "$PORT" &
UDP_PID=$!
sleep 1

echo "[*] Sending UDP message..."
kn-sock send-udp localhost "$PORT" "Hello from UDP test"

sleep 1
kill $UDP_PID

echo "[*] Starting file server..."
kn-sock run-file-server "$PORT" "$TMP_DIR" &
FILE_SERVER_PID=$!
sleep 1

echo "[*] Sending test file..."
kn-sock send-file localhost "$PORT" "$TEST_FILE"
sleep 1

if [[ -f "$RECEIVED_FILE" ]]; then
  echo "[✔] File transfer successful: $RECEIVED_FILE"
else
  echo "[✘] File transfer failed."
fi

# Final cleanup handled by trap
