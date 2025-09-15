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

server = VideoChatServer(
    host='0.0.0.0',
    video_port=9000,
    audio_port=9001,
    text_port=9002,
    max_clients_per_room=10,
    enable_audio=True,
    enable_video=True,
    video_quality=70,
    audio_sample_rate=44100
)
server.start()
```

### Custom Client Configuration

```python
from kn_sock.video_chat import VideoChatClient

client = VideoChatClient(
    server_ip='192.168.1.10',
    video_port=9000,
    audio_port=9001,
    text_port=9002,
    room='conference',
    nickname='john',
    enable_audio=True,
    enable_video=True,
    video_width=640,
    video_height=480,
    audio_channels=1,
    audio_sample_rate=44100
)
client.start()
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
        text_port=port_base + 2,
        max_clients_per_room=20
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

```python
from kn_sock.video_chat import VideoChatClient

class ClassroomClient(VideoChatClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_teacher = kwargs.get('is_teacher', False)
    
    def on_message_received(self, sender, message):
        """Handle incoming messages"""
        if self.is_teacher:
            # Teachers can see all messages
            print(f"[{sender}]: {message}")
        else:
            # Students only see teacher messages and their own
            if sender == "teacher" or sender == self.nickname:
                print(f"[{sender}]: {message}")
    
    def on_user_joined(self, nickname):
        """Handle user joining"""
        if self.is_teacher:
            print(f"Student {nickname} joined the class")
        else:
            print(f"User {nickname} joined")

# Teacher client
teacher = ClassroomClient(
    server_ip='192.168.1.10',
    room='math101',
    nickname='teacher',
    is_teacher=True
)
teacher.start()

# Student client
student = ClassroomClient(
    server_ip='192.168.1.10',
    room='math101',
    nickname='student1',
    is_teacher=False
)
student.start()
```

### Family Video Chat

```python
from kn_sock.video_chat import VideoChatClient

class FamilyChatClient(VideoChatClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.family_members = kwargs.get('family_members', [])
    
    def on_user_joined(self, nickname):
        """Welcome family members"""
        if nickname in self.family_members:
            self.send_message(f"Welcome back, {nickname}!")
        else:
            self.send_message(f"Welcome, {nickname}!")
    
    def on_user_left(self, nickname):
        """Say goodbye to family members"""
        if nickname in self.family_members:
            self.send_message(f"See you later, {nickname}!")

# Family members
family_members = ["mom", "dad", "sister", "brother"]

# Create family chat client
family_client = FamilyChatClient(
    server_ip='192.168.1.10',
    room='family',
    nickname='me',
    family_members=family_members
)
family_client.start()
```

## Performance Optimization

### Bandwidth Optimization

```python
from kn_sock.video_chat import VideoChatClient

# For slow connections
client = VideoChatClient(
    server_ip='remote-server.com',
    room='meeting',
    nickname='user',
    video_width=320,  # Lower resolution
    video_height=240,
    video_quality=50,  # Lower quality
    enable_audio=True,
    enable_video=True
)

# For high-quality connections
client = VideoChatClient(
    server_ip='local-server',
    room='meeting',
    nickname='user',
    video_width=1280,  # Higher resolution
    video_height=720,
    video_quality=90,  # Higher quality
    enable_audio=True,
    enable_video=True
)
```

### Audio Optimization

```python
from kn_sock.video_chat import VideoChatClient

# For voice-only meetings
client = VideoChatClient(
    server_ip='192.168.1.10',
    room='voice-meeting',
    nickname='user',
    enable_audio=True,
    enable_video=False,  # Disable video for voice-only
    audio_sample_rate=22050,  # Lower sample rate
    audio_channels=1  # Mono audio
)

# For music/audio quality
client = VideoChatClient(
    server_ip='192.168.1.10',
    room='music-room',
    nickname='user',
    enable_audio=True,
    enable_video=True,
    audio_sample_rate=48000,  # Higher sample rate
    audio_channels=2  # Stereo audio
)
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

### Audio/Video Issues

```python
from kn_sock.video_chat import VideoChatClient

# Test audio and video separately
def test_media():
    try:
        client = VideoChatClient(
            server_ip='192.168.1.10',
            room='test',
            nickname='tester',
            enable_audio=True,
            enable_video=True
        )
        
        # Test video
        if client.test_video():
            print("✓ Video working")
        else:
            print("✗ Video not working")
        
        # Test audio
        if client.test_audio():
            print("✓ Audio working")
        else:
            print("✗ Audio not working")
            
    except Exception as e:
        print(f"Media test failed: {e}")

test_media()
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