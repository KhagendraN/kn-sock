from kn_sock.video_chat import VideoChatClient
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Video Chat Client (No Audio)')
    parser.add_argument('server_ip', help='Server IP address')
    parser.add_argument('room', help='Room name to join')
    parser.add_argument('nickname', help='Your nickname')
    parser.add_argument('--video-port', type=int, default=9000, help='Video port (default: 9000)')
    parser.add_argument('--audio-port', type=int, default=9001, help='Audio port (default: 9001)')
    parser.add_argument('--text-port', type=int, default=9002, help='Text port (default: 9002)')
    
    args = parser.parse_args()
    
    print("🎥 Video Chat Client (Audio Disabled)")
    print("=" * 40)
    print("Controls:")
    print("  - Press 'v' to toggle video on/off")
    print("  - Press 'q' to quit")
    print("  - Type messages in the terminal and press Enter")
    print()
    
    client = VideoChatClient(
        server_ip=args.server_ip,
        video_port=args.video_port,
        audio_port=args.audio_port,
        text_port=args.text_port,
        room=args.room,
        nickname=args.nickname,
        enable_audio=False  # Disable audio
    )
    
    print(f'Connecting to video chat server at {args.server_ip}:{args.video_port}/{args.audio_port}/{args.text_port} in room "{args.room}" as "{args.nickname}"...')
    print('Features: video chat, text messaging, video on/off (audio disabled)')
    
    client.start()
    try:
        while client.running:
            pass
    except KeyboardInterrupt:
        print('Client stopped.') 