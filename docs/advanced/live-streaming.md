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

## Related Topics

- **[Video Chat](video-chat.md)** - For real-time video communication
- **[TCP Protocol](../protocols/tcp.md)** - For underlying transport
- **[API Reference](../api-reference.md)** - Complete function documentation 