# Live Streaming

kn-sock provides advanced live video and audio streaming capabilities with multi-video support, adaptive bitrate, and smooth playback.

## Overview

Live streaming features in kn-sock:
- **Multi-Video Support**: Server can offer multiple videos; clients select which to play
- **Adaptive Bitrate**: Server adjusts video quality per client based on buffer feedback
- **Jitter Buffer**: Client-side buffering for smooth video/audio playback
- **Robust Audio Protocol**: Audio stream uses magic numbers and timestamps for resynchronization
- **Real-time Feedback**: Client sends buffer status to server for quality adjustment

## Basic Live Streaming

### Live Stream Server

```python
from kn_sock import start_live_stream

# Start a live stream server with multiple videos
start_live_stream(9000, ["video1.mp4", "video2.mp4", "video3.mp4"])

# Or with a single video
start_live_stream(9000, ["video.mp4"])
```

### Live Stream Client

```python
from kn_sock import connect_to_live_server

# Connect to a live stream server
connect_to_live_server("192.168.1.10", 9000)
```

## Advanced Usage

### Custom Server Configuration

```python
from kn_sock.live_stream import LiveStreamServer

# Server with custom configuration
server = LiveStreamServer(
    video_paths=["video1.mp4", "video2.mp4"],
    host='0.0.0.0',
    video_port=8000,
    audio_port=8001,
    control_port=8010
)
server.start()
```

### Custom Client Configuration

```python
from kn_sock.live_stream import LiveStreamClient

# Client with custom buffer settings
client = LiveStreamClient(
    host='127.0.0.1',
    video_port=8000,
    audio_port=8001,
    control_port=8010,
    video_buffer_ms=200,  # 200ms video buffer
    audio_buffer_ms=100,  # 100ms audio buffer
    video_fps=30
)
client.start()
```

## CLI Usage

### Start Live Stream Server

```bash
# Start with multiple videos
kn-sock run-live-server 9000 video1.mp4 video2.mp4 video3.mp4

# Start with custom host and audio port
kn-sock run-live-server 9000 video.mp4 --host 0.0.0.0 --audio-port 9001
```

### Connect as Live Stream Client

```bash
# Connect to server
kn-sock connect-live-server 192.168.1.10 9000

# Connect with custom audio port
kn-sock connect-live-server 192.168.1.10 9000 --audio-port 9001
```

## How It Works

### 1. Server Setup

The server extracts audio from video files using FFmpeg and prepares for streaming:

```python
from kn_sock.live_stream import LiveStreamServer

server = LiveStreamServer(
    video_paths=["movie1.mp4", "movie2.mp4", "documentary.mp4"],
    host='0.0.0.0',
    video_port=9000,
    audio_port=9001,
    control_port=9010
)

print("Available videos:")
for i, video in enumerate(server.video_paths):
    print(f"{i+1}. {video}")

server.start()
```

### 2. Client Connection

Clients connect to video, audio, and control ports:

```python
from kn_sock.live_stream import LiveStreamClient

client = LiveStreamClient(
    host='192.168.1.10',
    video_port=9000,
    audio_port=9001,
    control_port=9010,
    video_buffer_ms=300,  # Larger buffer for slower connections
    audio_buffer_ms=150,
    video_fps=25  # Lower FPS for bandwidth optimization
)

client.start()
```

### 3. Video Selection

If multiple videos are available, clients are prompted to select one:

```python
# The client will automatically show available videos
# and allow selection if multiple videos are offered
```

### 4. Adaptive Streaming

The server adjusts video quality based on client feedback:

```python
# Server automatically adjusts JPEG quality (40-90) based on:
# - Client buffer levels
# - Network conditions
# - Client feedback
```

## Protocol Details

### Video Protocol

Each video frame is sent with timestamp and length information:

```
[8-byte timestamp][4-byte length][JPEG data]
```

### Audio Protocol

Audio chunks include magic numbers and timestamps for synchronization:

```
[4-byte magic][8-byte timestamp][4-byte length][audio data]
```

### Control Protocol

Clients send JSON feedback for adaptive quality:

```json
{
    "buffer_level": 0.2,
    "network_quality": "good",
    "timestamp": 1234567890.123
}
```

## Configuration Options

### Server Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `video_paths` | List of video file paths | Required |
| `host` | Host to bind | '0.0.0.0' |
| `video_port` | Port for video stream | 8000 |
| `audio_port` | Port for audio stream | 8001 |
| `control_port` | Port for control messages | video_port + 10 |

### Client Configuration  

| Parameter | Description | Default |
|-----------|-------------|---------|
| `host` | Server host | '127.0.0.1' |
| `video_port` | Video stream port | 8000 |
| `audio_port` | Audio stream port | 8001 |
| `control_port` | Control port | video_port + 10 |
| `video_buffer_ms` | Video buffer size (ms) | 200 |
| `audio_buffer_ms` | Audio buffer size (ms) | 200 |
| `video_fps` | Target video FPS | 30 |

## Use Cases

### Multi-Room Video Streaming

```python
from kn_sock.live_stream import LiveStreamServer
import threading

def start_room(room_name, videos, port_base):
    """Start a streaming room"""
    server = LiveStreamServer(
        video_paths=videos,
        host='0.0.0.0',
        video_port=port_base,
        audio_port=port_base + 1,
        control_port=port_base + 10
    )
    
    print(f"Starting {room_name} on ports {port_base}, {port_base+1}, {port_base+10}")
    server.start()

# Start multiple rooms
rooms = [
    ("Action Movies", ["action1.mp4", "action2.mp4"], 9000),
    ("Comedy Movies", ["comedy1.mp4", "comedy2.mp4"], 9100),
    ("Documentaries", ["doc1.mp4", "doc2.mp4"], 9200)
]

for room_name, videos, port_base in rooms:
    thread = threading.Thread(
        target=start_room,
        args=(room_name, videos, port_base),
        daemon=True
    )
    thread.start()
```

### Adaptive Quality Streaming

The `LiveStreamServer` includes built-in adaptive quality streaming. The server automatically adjusts JPEG quality (40-90%) based on client buffer feedback sent through the control port.

```python
from kn_sock.live_stream import LiveStreamServer
import time

# Start server with adaptive quality enabled
server = LiveStreamServer(
    video_paths=["movie.mp4"],
    host='0.0.0.0',
    video_port=9000,
    audio_port=9001,
    control_port=9010  # Control port for adaptive quality feedback
)

print("Starting adaptive quality live stream server...")
print("Server will automatically adjust quality based on client feedback:")
print("  - Low buffer (< 10%): Reduce quality to improve streaming")
print("  - High buffer (> 30%): Increase quality for better experience")

server.start()
```

### Multi-Video Room Setup

```python
from kn_sock.live_stream import LiveStreamServer
import threading

def start_room(room_name, videos, port_base):
    """Start a streaming room with multiple videos"""
    server = LiveStreamServer(
        video_paths=videos,
        host='0.0.0.0',
        video_port=port_base,
        audio_port=port_base + 1,
        control_port=port_base + 10
    )
    
    print(f"Room '{room_name}' starting on ports {port_base}-{port_base+10}")
    print(f"Available videos: {videos}")
    server.start()

# Start multiple streaming rooms
rooms = [
    ("Action Movies", ["action1.mp4", "action2.mp4"], 9000),
    ("Documentaries", ["doc1.mp4", "doc2.mp4"], 9100),
    ("Comedy", ["comedy1.mp4", "comedy2.mp4"], 9200)
]

for room_name, videos, port_base in rooms:
    thread = threading.Thread(
        target=start_room,
        args=(room_name, videos, port_base),
        daemon=True
    )
    thread.start()
```

### Bandwidth Monitoring

```python
from kn_sock.live_stream import LiveStreamClient
import time
import threading

class MonitoredClient(LiveStreamClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bytes_received = 0
        self.start_time = time.time()
        self._monitoring = True
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_bandwidth, daemon=True)
        self.monitor_thread.start()
    
    def _monitor_bandwidth(self):
        """Monitor bandwidth usage in background thread"""
        while self._monitoring and self._running.is_set():
            time.sleep(5)  # Check every 5 seconds
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                bandwidth_mbps = (self.bytes_received * 8) / (elapsed * 1024 * 1024)
                print(f"Current bandwidth: {bandwidth_mbps:.2f} Mbps")
    
    def stop(self):
        """Override stop to disable monitoring"""
        self._monitoring = False
        super().stop()

# Usage
client = MonitoredClient(
    host='192.168.1.10',
    video_port=9000,
    audio_port=9001
)
client.start()
```

## Performance Optimization

### Buffer Tuning

```python
# For high-latency networks
client = LiveStreamClient(
    host='remote-server.com',
    video_buffer_ms=500,  # Larger buffer
    audio_buffer_ms=200,
    video_fps=24  # Lower FPS
)

# For low-latency requirements
client = LiveStreamClient(
    host='local-server',
    video_buffer_ms=100,  # Smaller buffer
    audio_buffer_ms=50,
    video_fps=60  # Higher FPS
)
```

### Quality Configuration

```python
# Server with multiple videos for selection
server = LiveStreamServer(
    video_paths=["low_quality.mp4", "medium_quality.mp4", "high_quality.mp4"],
    host='0.0.0.0',
    video_port=9000,
    audio_port=9001,
    control_port=9010  # Control port for adaptive quality
)
server.start()

# Client configuration for different network conditions
# Note: Quality adaptation is handled automatically by the server
# based on client feedback sent through the control port

# For high-latency networks - larger buffers
client = LiveStreamClient(
    host='remote-server.com',
    video_port=9000,
    audio_port=9001,
    control_port=9010,
    video_buffer_ms=500,  # Larger buffer for stability
    audio_buffer_ms=200,
    video_fps=24  # Lower FPS can help with bandwidth
)

# For low-latency requirements - smaller buffers  
client = LiveStreamClient(
    host='local-server',
    video_port=9000,
    audio_port=9001,
    control_port=9010,
    video_buffer_ms=100,  # Smaller buffer for lower latency
    audio_buffer_ms=50,
    video_fps=30  # Standard FPS
)
```

## Error Handling

### Network Issues

```python
from kn_sock.live_stream import LiveStreamClient
import time

def resilient_client():
    while True:
        try:
            client = LiveStreamClient(
                host='192.168.1.10',
                video_port=9000,
                audio_port=9001
            )
            client.start()
        except Exception as e:
            print(f"Connection lost: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)

resilient_client()
```

### Video File Issues

```python
from kn_sock.live_stream import LiveStreamServer
import os

def validate_videos(video_paths):
    """Validate video files before starting server"""
    valid_videos = []
    
    for video_path in video_paths:
        if os.path.exists(video_path):
            # Check if it's a valid video file
            if video_path.lower().endswith(('.mp4', '.avi', '.mkv')):
                valid_videos.append(video_path)
            else:
                print(f"Warning: {video_path} is not a supported video format")
        else:
            print(f"Warning: {video_path} not found")
    
    return valid_videos

video_paths = ["video1.mp4", "video2.mp4", "invalid.txt"]
valid_videos = validate_videos(video_paths)

if valid_videos:
    server = LiveStreamServer(video_paths=valid_videos)
    server.start()
else:
    print("No valid videos found")
```

## Requirements

### Python Dependencies

```bash
pip install opencv-python pyaudio numpy
```

### System Dependencies

- **FFmpeg**: Required for audio extraction
  ```bash
  # Ubuntu/Debian
  sudo apt-get install ffmpeg
  
  # macOS
  brew install ffmpeg
  
  # Windows
  # Download from https://ffmpeg.org/download.html
  ```

### Network Requirements

- TCP ports for video, audio, and control streams
- Sufficient bandwidth for video streaming
- Low latency for real-time streaming

## Troubleshooting

### Common Issues

1. **Video not playing**
   - Check video file format (mp4 recommended)
   - Ensure FFmpeg is installed
   - Verify video file is not corrupted

2. **Audio issues**
   - Check PyAudio installation
   - Verify audio drivers
   - Test with audio-only files

3. **Poor performance**
   - Reduce video FPS
   - Increase buffer sizes
   - Check network bandwidth

4. **Connection issues**
   - Verify firewall settings
   - Check port availability
   - Test network connectivity

### Diagnostic Tools

```python
# Test video file compatibility
from kn_sock.live_stream import LiveStreamServer

def test_video(video_path):
    try:
        server = LiveStreamServer(video_paths=[video_path])
        print(f"✓ {video_path} is compatible")
        return True
    except Exception as e:
        print(f"✗ {video_path} failed: {e}")
        return False

# Test multiple videos
videos = ["video1.mp4", "video2.avi", "video3.mkv"]
for video in videos:
    test_video(video)
```

## Related Topics

- **[Video Chat](video-chat.md)** - For real-time video communication
- **[TCP Protocol](../protocols/tcp.md)** - For underlying transport
- **[API Reference](../api-reference.md)** - Complete function documentation 