# Live Streaming Utilities

kn-sock supports real-time video and audio streaming over the network, using FFmpeg and OpenCV.  

Use these tools for demos, surveillance, or experimental real-time media pipelines.

## CLI Commands

### 1. Start a Live Video/Audio Stream Server

Stream one or more video files (with audio) to connected clients.

| Command                                                   | Description                                 |
|-----------------------------------------------------------|---------------------------------------------|
| `run-live-server <port> <video_paths...> [--host <host>] [--audio-port <audio_port>]` | Start live streaming server |

**Example:**
```sh
docker-compose run --rm knsock run-live-server 9002 demo.mp4
# Or to specify host/audio port:
docker-compose run --rm knsock run-live-server 9002 demo.mp4 --host 0.0.0.0 --audio-port 9003
```
**Output:**
```
[LIVE][SERVER] Streaming video(s): demo.mp4 on 0.0.0.0:9002, audio on 0.0.0.0:9003
```

### 2. Connect to a Live Video/Audio Stream

Connect as a client to the live stream server and display the stream.

| Command                                                   | Description                   |
|-----------------------------------------------------------|-------------------------------|
| `connect-live-server <ip> <video_port> [--audio-port <audio_port>]` | Connect and view stream |

**Example:**
```sh
docker-compose run --rm knsock connect-live-server 172.18.0.2 9002
# Specify audio port if needed:
docker-compose run --rm knsock connect-live-server 172.18.0.2 9002 --audio-port 9003
```
**Output:**
```
[LIVE][CLIENT] Connecting to video at 172.18.0.2:9002 (audio: 9003)
[LIVE][CLIENT] Displaying video stream...
```

#### Options Table
| Option         | Description                           |
|----------------|---------------------------------------|
| `<port>`       | Video port for server/client          |
| `<video_paths>`| One or more video file paths to stream (server) |
| `<host>`       | Host to bind (default: 0.0.0.0; server only) |
| `<audio_port>` | Audio port (default: <port>+1)       |
| `<ip>`         | Server IP address (client only)      |

## Python API

### Start a Live Stream Server
```python
from kn_sock import start_live_stream

# Stream video and audio from local files on port 9002 (video), 9003 (audio)
start_live_stream(9002, ["demo.mp4"])
```

### Connect as a Stream Client
```python
from kn_sock import connect_to_live_server

connect_to_live_server("127.0.0.1", 9002)  # (video port, default audio port is 9003)
```

### Sample Output
**Server terminal:**
```
[LIVE][SERVER] Streaming video(s): demo.mp4 on 0.0.0.0:9002, audio on 0.0.0.0:9003
[LIVE][SERVER] Waiting for clients...
```

**Client terminal:**
```
[LIVE][CLIENT] Connecting to video at 172.18.0.2:9002 (audio: 9003)
[LIVE][CLIENT] Displaying video stream...
```

## Known Issues & Troubleshooting
| Issue                        | Symptom/Output                              | Solution                                           |
|------------------------------|---------------------------------------------|----------------------------------------------------|
| Missing dependencies         | `ImportError: libGL.so.1...`                | Install OpenCV and required system libraries       |
| Video not displayed          | No window appears, blank screen             | Check local GUI/X11 settings in container          |
| Connection refused           | `ConnectionRefusedError`                    | Ensure server is running, ports are open           |
| Audio issues                 | No sound, audio errors                      | Confirm audio port and codec compatibility         |

## Testing
### Manual Test
Start the server (with a sample video in the container):
```sh
docker-compose run --rm knsock run-live-server 9002 demo.mp4
```

In another terminal, connect as a client:
```sh
docker-compose run --rm knsock connect-live-server <server-ip> 9002
# Example: connect-live-server 172.18.0.2 9002
```

Observe video window/audio output on the client side.

**Note:** Live video streaming may require proper video files and local display access in Docker environments. Test outside Docker if GUI support is limited.