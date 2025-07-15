from kn_sock.video_chat import VideoChatServer

if __name__ == '__main__':
    server = VideoChatServer(host='0.0.0.0', video_port=9000, audio_port=9001, text_port=9002)
    print('Video chat server started on ports:')
    print('  - 9000 (video)')
    print('  - 9001 (audio)')
    print('  - 9002 (text chat)')
    print('Clients can join different rooms and set their nickname.')
    print('Features: video/audio chat, text messaging, mute/unmute, video on/off')
    # The server will handle multiple rooms and nicknames automatically.
    server.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Server stopped.') 