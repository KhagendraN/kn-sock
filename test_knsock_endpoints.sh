#!/bin/bash

set -e

# Helper: Wait for a service port to be open in the container
wait_for_port() {
  local ip="$1"
  local port="$2"
  local timeout=10
  echo "Waiting for $ip:$port to be open..."
  for ((i=0;i<timeout;i++)); do
    if docker run --rm knsock:latest python -c "import socket; s=socket.socket(); s.settimeout(1); s.connect(('${ip}', ${port}))" 2>/dev/null; then
      return 0
    fi
    sleep 1
  done
  echo "Timeout waiting for $ip:$port"
  return 1
}

# Helper: Start a server and return the container ID
start_server() {
  local name=$1
  shift
  docker-compose run -d --name "$name" knsock "$@"
}

# Helper: Clean up container by name
cleanup_container() {
  docker rm -f "$1" >/dev/null 2>&1 || true
}

# Get fresh network
docker-compose down --remove-orphans

# Test results log
LOGFILE="knsock_test_results.log"
> "$LOGFILE"

# Get the current subnet
SUBNET=$(docker network inspect kn-sock_default | grep Subnet | head -1 | awk -F'"' '{print $4}')
SERVER_IP=""
# Use docker inspect to get server IP after starting container

########### TCP Test ###########
echo "=== TCP Echo Test ===" | tee -a "$LOGFILE"
cleanup_container tcpserver
tcp_server_cid=$(start_server tcpserver run-tcp-server 8080)
sleep 2
SERVER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' tcpserver)
echo "Server IP: $SERVER_IP"
sleep 1
docker-compose run --rm knsock send-tcp $SERVER_IP 8080 "Hello TCP" | tee -a "$LOGFILE"
cleanup_container tcpserver

########### UDP Test ###########
echo "=== UDP Echo Test ===" | tee -a "$LOGFILE"
cleanup_container udpserver
udp_server_cid=$(start_server udpserver run-udp-server 8081)
sleep 2
SERVER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' udpserver)
docker-compose run --rm knsock send-udp $SERVER_IP 8081 "Hello UDP" | tee -a "$LOGFILE"
cleanup_container udpserver

########### File Transfer Test ###########
echo "=== File Transfer Test ===" | tee -a "$LOGFILE"
touch testfile.txt
cleanup_container fileserver
file_server_cid=$(start_server fileserver run-file-server 9000 /tmp)
sleep 2
SERVER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' fileserver)
docker-compose run --rm -v "$(pwd):/app" knsock send-file $SERVER_IP 9000 testfile.txt | tee -a "$LOGFILE"
cleanup_container fileserver

########### WebSocket Test ###########
echo "=== WebSocket Echo Test ===" | tee -a "$LOGFILE"
cleanup_container wsserver
ws_server_cid=$(start_server wsserver run-websocket-server 7000)
sleep 2
SERVER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' wsserver)
docker-compose run --rm knsock websocket-client $SERVER_IP 7000 "Hello WebSocket" | tee -a "$LOGFILE"
cleanup_container wsserver

########### HTTP Test ###########
echo "=== HTTP Server Test ===" | tee -a "$LOGFILE"
cleanup_container httpserver
http_server_cid=$(docker-compose run -d --name httpserver -p 8085:8085 knsock run-http-server 8085)
sleep 2
# Test using curl from host
echo "HTTP GET result:" | tee -a "$LOGFILE"
curl -s http://localhost:8085/ | tee -a "$LOGFILE"
cleanup_container httpserver

########### PubSub Test ###########
echo "=== PubSub Test ===" | tee -a "$LOGFILE"
cleanup_container pubsubserver
pubsub_server_cid=$(start_server pubsubserver run-pubsub-server 8000)
sleep 2
SERVER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' pubsubserver)
docker-compose run --rm knsock pubsub-client $SERVER_IP 8000 subscribe test | tee -a "$LOGFILE"
cleanup_container pubsubserver

########### RPC Test ###########
echo "=== RPC Test ===" | tee -a "$LOGFILE"
cleanup_container rpcserver
rpc_server_cid=$(start_server rpcserver run-rpc-server 9001)
sleep 2
SERVER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' rpcserver)
docker-compose run --rm knsock rpc-client $SERVER_IP 9001 add 1 2 | tee -a "$LOGFILE"
cleanup_container rpcserver

########### SSL TCP Test ###########
echo "=== SSL TCP Test ===" | tee -a "$LOGFILE"
# NOTE: This requires certificates and will fail unless configured. Add manual steps if you want to test SSL.

echo "SSL TCP test skipped (requires certs setup)" | tee -a "$LOGFILE"

echo ""
echo "=============================="
echo "  kn-sock Endpoint Test Log"
echo "  See $LOGFILE for details."
echo "=============================="

