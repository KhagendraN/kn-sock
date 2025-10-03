# Video Chat

kn-sock provides real-time multi-client video chat with voice, allowing multiple users to join rooms and communicate with both video and audio in real time.

## Overview

Video chat features in kn-sock:
- **Multi-client support**: Multiple users can join the same room and see/hear each other
- **Rooms/Channels**: Users can join named rooms; only users in the same room see/hear each other
- **User Nicknames**: Each client can set a nickname, which is shared with the server and other clients
- **Text Chat**: Real-time text messaging with chat overlay on video window
- **Mute/Unmute**: Toggle audio on/off with keyboard shortcut
- **Video On/Off**: Toggle video camera on/off with keyboard shortcut
- **Real-time video and audio**: Uses OpenCV for video and PyAudio for audio
- **Simple API**: Easy to start a server or connect as a client

## Basic Video Chat

### Video Chat Server

```python
from kn_sock.video_chat import VideoChatServer

server = VideoChatServer(host='0.0.0.0', video_port=9000, audio_port=9001, text_port=9002)
server.start()
print('Video chat server started on ports 9000 (video), 9001 (audio), and 9002 (text).')

# Keep the server running
try:
    while True:
        pass
except KeyboardInterrupt:
    print('Server stopped.')
```

### Video Chat Client

```python
from kn_sock.video_chat import VideoChatClient

client = VideoChatClient(
    server_ip='127.0.0.1', 
    video_port=9000, 
    audio_port=9001, 
    text_port=9002, 
    room='myroom', 
    nickname='alice'
)
client.start()
print('Connected to video chat server in room "myroom" as "alice".')

# Keep the client running
try:
    while client.running:
        pass
except KeyboardInterrupt:
    print('Client stopped.')
```

## Advanced Configuration

### Custom Server Configuration

```python
from kn_sock.video_chat import VideoChatServer

# Server supports only basic configuration parameters
server = VideoChatServer(
    host='0.0.0.0',
    video_port=9000,
    audio_port=9001,
    text_port=9002
)
server.start()

print("Video chat server started:")
print(f"  - Video port: {server.video_port}")  
print(f"  - Audio port: {server.audio_port}")
print(f"  - Text chat port: {server.text_port}")
print("  - Supports multiple rooms")
print("  - Users can join with custom nicknames")
```

### Custom Client Configuration

```python
from kn_sock.video_chat import VideoChatClient

# Client configuration with available parameters
client = VideoChatClient(
    server_ip='192.168.1.10',
    video_port=9000,
    audio_port=9001,
    text_port=9002,
    room='conference',
    nickname='john',
    enable_audio=True  # Enable/disable audio functionality
)
client.start()
```

### Multi-Room Setup

```python
from kn_sock.video_chat import VideoChatServer
import threading

# Start multiple servers for different rooms
def start_server_for_room(room_name, port_base):
    server = VideoChatServer(
        host='0.0.0.0',
        video_port=port_base,
        audio_port=port_base + 1, 
        text_port=port_base + 2
    )
    
    print(f"Room '{room_name}' starting on ports {port_base}-{port_base+2}")
    server.start()

# Configure different rooms
rooms = [
    ("lobby", 9000),
    ("meeting1", 9100), 
    ("meeting2", 9200)
]

for room_name, port_base in rooms:
    thread = threading.Thread(
        target=start_server_for_room,
        args=(room_name, port_base),
        daemon=True
    )
    thread.start()
```
## Troubleshooting

### Common Issues and Solutions

#### Audio Issues (Most Common)

If you encounter PyAudio assertion errors or audio crashes:

1. **Disable audio temporarily:**
   ```bash
   python examples/video_chat_client.py 127.0.0.1 myroom alice --no-audio
   ```

2. **Use the no-audio client:**
   ```bash
   python examples/video_chat_client_no_audio.py 127.0.0.1 myroom alice
   ```

3. **Test audio separately:**
   ```bash
   python examples/test_audio_only.py
   ```

4. **Install audio drivers (Arch Linux):**
   ```bash
   sudo pacman -S pulseaudio pulseaudio-alsa
   ```

5. **Set audio environment variables:**
   ```bash
   export PULSE_SERVER=unix:/tmp/pulse-socket
   export ALSA_PCM_CARD=0
   ```

#### Display Issues

```bash
# Set display backend for OpenCV
export QT_QPA_PLATFORM=xcb
```

#### Camera Issues

- Make sure your camera is not in use by another application
- Check camera permissions
- Try different camera device numbers if you have multiple cameras

#### Dependencies

```bash
# Install required packages
pip install opencv-python pyaudio numpy
```

**Note:** The video chat feature works perfectly without audio. If you have persistent audio issues, you can still use video and text chat functionality.

## Requirements

### Python Dependencies

```bash
pip install opencv-python pyaudio numpy
```

### Hardware Requirements

- **Webcam**: For video functionality
- **Microphone**: For audio functionality
- **Speakers/Headphones**: For audio output

### Network Requirements

- TCP ports for video, audio, and text streams (default: 9000, 9001, and 9002)
- Sufficient bandwidth for video streaming
- Low latency for real-time communication

## Related Topics

- **[Live Streaming](live-streaming.md)** - For one-to-many video streaming
- **[TCP Protocol](../protocols/tcp.md)** - For underlying transport
- **[API Reference](../api-reference.md)** - Complete function documentation 