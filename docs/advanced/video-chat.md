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
```

## Client Controls

When the video window is active, you can use these keyboard shortcuts:

- **`m`**: Mute/unmute your microphone
- **`v`**: Toggle your video camera on/off
- **`q`**: Quit the application

## Text Chat

- Type messages in the terminal and press Enter to send
- Chat messages appear as an overlay on the video window
- Messages include timestamps and sender nicknames
- Only users in the same room receive the messages

## CLI Usage

### Start Video Chat Server

```bash
# Start with default settings
kn-sock run-video-chat-server

# Start with custom configuration
kn-sock run-video-chat-server --host 0.0.0.0 --video-port 9000 --audio-port 9001 --text-port 9002
```

### Connect to Video Chat Server

```bash
# Connect with room and nickname
kn-sock connect-video-chat 127.0.0.1 myroom alice

# Connect with custom ports
kn-sock connect-video-chat 192.168.1.10 conference john --video-port 9000 --audio-port 9001 --text-port 9002
```

## Use Cases

### Multi-Room Conference System

```python
from kn_sock.video_chat import VideoChatServer
import threading

def start_conference_room(room_name, port_base):
    """Start a conference room"""
    server = VideoChatServer(
        host='0.0.0.0',
        video_port=port_base,
        audio_port=port_base + 1,
        text_port=port_base + 2
    )
    
    print(f"Starting conference room '{room_name}' on ports {port_base}, {port_base+1}, {port_base+2}")
    server.start()

# Start multiple conference rooms
rooms = [
    ("Engineering", 9000),
    ("Marketing", 9100),
    ("Sales", 9200),
    ("Support", 9300)
]

for room_name, port_base in rooms:
    thread = threading.Thread(
        target=start_conference_room,
        args=(room_name, port_base),
        daemon=True
    )
    thread.start()
```

### Classroom Video Chat

### Group Video Chat Example

```python
from kn_sock.video_chat import VideoChatClient
import threading
import time

def start_group_client(room, nickname, server_ip='192.168.1.10'):
    """Start a video chat client for group communication"""
    client = VideoChatClient(
        server_ip=server_ip,
        video_port=9000,
        audio_port=9001,
        text_port=9002,
        room=room,
        nickname=nickname,
        enable_audio=True
    )
    
    print(f"Starting {nickname} in room '{room}'")
    client.start()
    
    # Keep client running
    try:
        while client.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"{nickname} is leaving the chat")
        client.stop()

# Start multiple clients for group chat
participants = [
    ("meeting_room", "alice"),
    ("meeting_room", "bob"), 
    ("meeting_room", "charlie")
]

threads = []
for room, nickname in participants:
    thread = threading.Thread(
        target=start_group_client,
        args=(room, nickname),
        daemon=True
    )
    thread.start()
    threads.append(thread)
    time.sleep(1)  # Stagger connections

# Keep main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down group chat")
```

### Multiple Room Setup

```python
from kn_sock.video_chat import VideoChatServer
import threading
import time

def start_room_server(room_config):
    """Start a video chat server for a specific room configuration"""
    room_name, port_base = room_config
    
    server = VideoChatServer(
        host='0.0.0.0',
        video_port=port_base,
        audio_port=port_base + 1,
        text_port=port_base + 2
    )
    
    print(f"Starting room '{room_name}' on ports {port_base}, {port_base+1}, {port_base+2}")
    server.start()
    
    # Keep server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"Room '{room_name}' shutting down")

# Configure multiple rooms
room_configs = [
    ("General", 9000),
    ("Engineering", 9100), 
    ("Sales", 9200),
    ("Support", 9300)
]

# Start each room in its own thread
for room_config in room_configs:
    thread = threading.Thread(
        target=start_room_server,
        args=(room_config,),
        daemon=True
    )
    thread.start()

print("All video chat rooms started!")
print("Available rooms:")
for room_name, port_base in room_configs:
    print(f"  - {room_name}: video={port_base}, audio={port_base+1}, text={port_base+2}")

# Keep main process alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down all rooms")
```
    server_ip='192.168.1.10',
    room='family',
    nickname='me',
    family_members=family_members
)
family_client.start()
```

## Configuration Details

### Server Configuration

The `VideoChatServer` uses predefined settings optimized for real-time communication:

```python
from kn_sock.video_chat import VideoChatServer

# Server configuration (settings are fixed for optimal performance)
server = VideoChatServer(
    host='0.0.0.0',        # Host to bind to
    video_port=9000,       # Port for video stream
    audio_port=9001,       # Port for audio stream  
    text_port=9002         # Port for text chat
)

print("Video chat server configuration:")
print(f"  Video settings: 320x240 @ 15fps")
print(f"  Audio settings: 44.1kHz mono")
print(f"  Supports multiple rooms and users")

server.start()
```

### Client Configuration

```python
from kn_sock.video_chat import VideoChatClient

# Available client parameters
client = VideoChatClient(
    server_ip='192.168.1.10',  # Required: Server IP
    video_port=9000,           # Video stream port
    audio_port=9001,           # Audio stream port
    text_port=9002,            # Text chat port
    room='meeting',            # Room name to join
    nickname='alice',          # Your display name
    enable_audio=True          # Enable/disable audio
)

print(f"Connecting to room '{client.room}' as '{client.nickname}'")
print(f"Audio enabled: {client.enable_audio}")

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

## Error Handling

### Connection Issues

```python
from kn_sock.video_chat import VideoChatClient
import time

def resilient_video_chat():
    while True:
        try:
            client = VideoChatClient(
                server_ip='192.168.1.10',
                room='meeting',
                nickname='user'
            )
            client.start()
        except Exception as e:
            print(f"Connection lost: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)

resilient_video_chat()
```

### Server/Client Connection Issues

```python
from kn_sock.video_chat import VideoChatClient
import socket

# Test connection to server
def test_connection():
    try:
        # Test if server is reachable
        test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_sock.settimeout(5)
        result = test_sock.connect_ex(('192.168.1.10', 9000))
        test_sock.close()
        
        if result == 0:
            print("✓ Server is reachable")
            
            # Try to connect client
            client = VideoChatClient(
                server_ip='192.168.1.10',
                room='test',
                nickname='tester',
                enable_audio=True
            )
            print("✓ Client configured successfully")
            # Note: client.start() would begin streaming
            
        else:
            print("✗ Cannot reach server on port 9000")
            print("  - Check if server is running")
            print("  - Verify firewall settings")
            
    except Exception as e:
        print(f"Connection test failed: {e}")

test_connection()
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