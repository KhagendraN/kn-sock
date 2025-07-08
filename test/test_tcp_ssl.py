import os
import tempfile
import subprocess
import threading
import time
import pytest
import sys
import asyncio
import shutil

from kn_sock import start_ssl_tcp_server, send_ssl_tcp_message, start_async_ssl_tcp_server, send_ssl_tcp_message_async

pytestmark = pytest.mark.skipif(
    not shutil.which('openssl'), reason='openssl not available for test cert generation'
)

def generate_self_signed_cert(tmpdir):
    certfile = os.path.join(tmpdir, 'server.crt')
    keyfile = os.path.join(tmpdir, 'server.key')
    subprocess.check_call([
        'openssl', 'req', '-x509', '-nodes', '-days', '1',
        '-newkey', 'rsa:2048',
        '-keyout', keyfile,
        '-out', certfile,
        '-subj', '/CN=localhost'
    ], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    return certfile, keyfile

def test_ssl_tcp_sync():
    with tempfile.TemporaryDirectory() as tmpdir:
        certfile, keyfile = generate_self_signed_cert(tmpdir)
        port = 9443
        received = {}
        def handler(data, addr, client_socket):
            received['data'] = data
            client_socket.sendall(b'ACK:' + data)
        server_thread = threading.Thread(
            target=start_ssl_tcp_server,
            args=(port, handler, certfile, keyfile),
            kwargs={'require_client_cert': False},
            daemon=True
        )
        server_thread.start()
        time.sleep(1)
        send_ssl_tcp_message('localhost', port, 'hello ssl', cafile=certfile, verify=False)
        time.sleep(0.5)
        assert received['data'] == b'hello ssl'
        print('[SUCCESS] SSL TCP sync server/client')

@pytest.mark.asyncio
async def test_ssl_tcp_async():
    with tempfile.TemporaryDirectory() as tmpdir:
        certfile, keyfile = generate_self_signed_cert(tmpdir)
        port = 9444
        received = {}
        async def handler(data, addr, writer):
            received['data'] = data
            writer.write(b'ACK:' + data)
            await writer.drain()
        def run_server():
            asyncio.run(start_async_ssl_tcp_server(
                port,
                handler,
                certfile=certfile,
                keyfile=keyfile,
                require_client_cert=False
            ))
        server_thread = threading.Thread(
            target=run_server,
            daemon=True
        )
        server_thread.start()
        await asyncio.sleep(1)
        await send_ssl_tcp_message_async('localhost', port, 'hello ssl', cafile=certfile, verify=False)
        await asyncio.sleep(0.5)
        assert received['data'] == b'hello ssl'
        print('[SUCCESS] SSL TCP async server/client')

def test_tcp_connection_pool_ssl():
    from kn_sock import TCPConnectionPool
    import threading
    import time
    with tempfile.TemporaryDirectory() as tmpdir:
        certfile, keyfile = generate_self_signed_cert(tmpdir)
        port = 9553
        def echo_server():
            def handler(data, addr, client_socket):
                client_socket.sendall(b"ECHO:" + data)
            start_ssl_tcp_server(port, handler, certfile, keyfile, require_client_cert=False)
        server_thread = threading.Thread(target=echo_server, daemon=True)
        server_thread.start()
        time.sleep(1)
        pool = TCPConnectionPool('localhost', port, max_size=2, idle_timeout=5, ssl=True, cafile=certfile, verify=False)
        with pool.connection() as conn:
            conn.sendall(b"ssl pool test")
            data = conn.recv(1024)
            assert data == b"ECHO:ssl pool test"
        pool.closeall()
        print("[SUCCESS] TCPConnectionPool SSL/TLS") 