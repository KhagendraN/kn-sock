import os
import tempfile
import threading
import asyncio
import pytest
from kn_sock.file_transfer import send_file, start_file_server, send_file_async, start_file_server_async
from kn_sock.utils import get_free_port

@pytest.fixture
def temp_text_file():
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as f:
        f.write('hello world')
        f.flush()
        yield f.name
    os.remove(f.name)

@pytest.fixture
def temp_dir():
    d = tempfile.mkdtemp()
    yield d
    try:
        os.rmdir(d)
    except Exception:
        pass

def test_sync_file_transfer(temp_text_file, temp_dir):
    port = get_free_port()
    received_path = os.path.join(temp_dir, os.path.basename(temp_text_file))
    def server():
        start_file_server(port, temp_dir)
    server_thread = threading.Thread(target=server, daemon=True)
    server_thread.start()
    import time; time.sleep(0.5)
    send_file('localhost', port, temp_text_file)
    import time; time.sleep(0.5)
    assert os.path.exists(received_path)
    with open(received_path) as f:
        assert f.read() == 'hello world'
    print('[SUCCESS] Sync file transfer')

@pytest.mark.asyncio
async def test_async_file_transfer(temp_text_file, temp_dir):
    port = get_free_port()
    received_path = os.path.join(temp_dir, os.path.basename(temp_text_file))
    async def server():
        await start_file_server_async(port, temp_dir)
    server_task = asyncio.create_task(server())
    await asyncio.sleep(0.5)
    await send_file_async('localhost', port, temp_text_file)
    await asyncio.sleep(0.5)
    assert os.path.exists(received_path)
    with open(received_path) as f:
        assert f.read() == 'hello world'
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass
    print('[SUCCESS] Async file transfer') 