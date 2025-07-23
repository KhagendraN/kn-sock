import cmd
import sys
import socket
import threading
import time
from kn_sock.tcp import _get_socket_family, BUFFER_SIZE

class KnSockInteractiveCLI(cmd.Cmd):
    intro = 'Welcome to the kn-sock interactive CLI. Type help or ? to list commands.\n'
    prompt = '(kn-sock) '

    def __init__(self):
        super().__init__()
        self.connections = {}  # name -> socket
        self.default_conn = None
        self.history = []  # (direction, message)
        self.max_history = 10
        self.bg_receive = False
        self.bg_thread = None
        self._stop_bg = threading.Event()

    def do_connect(self, arg):
        'Connect to a server: connect <name> <host> <port>'
        parts = arg.strip().split()
        if len(parts) != 3:
            print('Usage: connect <name> <host> <port>')
            return
        name, host, port = parts
        try:
            port = int(port)
            family = _get_socket_family(host)
            s = socket.socket(family, socket.SOCK_STREAM)
            s.connect((host, port))
            self.connections[name] = s
            self.default_conn = name
            print(f'Connected to {host}:{port} as "{name}".')
        except Exception as e:
            print(f'Failed to connect: {e}')

    def do_list(self, arg):
        'List active connections: list'
        if not self.connections:
            print('No active connections.')
            return
        for name, s in self.connections.items():
            try:
                peer = s.getpeername()
            except Exception:
                peer = '(disconnected)'
            default = ' (default)' if name == self.default_conn else ''
            print(f'{name}: {peer}{default}')

    def do_send(self, arg):
        'Send a message: send <message> (to default connection)'
        if not self.default_conn or self.default_conn not in self.connections:
            print('No default connection. Use connect or select.')
            return
        s = self.connections[self.default_conn]
        try:
            s.sendall(arg.encode('utf-8'))
            self._add_history('sent', arg)
            print('Message sent.')
        except Exception as e:
            print(f'Failed to send: {e}')

    def do_receive(self, arg):
        'Receive a message: receive (from default connection)'
        if not self.default_conn or self.default_conn not in self.connections:
            print('No default connection. Use connect or select.')
            return
        s = self.connections[self.default_conn]
        try:
            data = s.recv(BUFFER_SIZE)
            if data:
                msg = data.decode("utf-8", errors="replace")
                self._add_history('recv', msg)
                print(f'Received: {msg}')
            else:
                print('No data received (connection may be closed).')
        except Exception as e:
            print(f'Failed to receive: {e}')

    def do_select(self, arg):
        'Select default connection: select <name>'
        name = arg.strip()
        if name in self.connections:
            self.default_conn = name
            print(f'Default connection set to "{name}".')
        else:
            print(f'No such connection: {name}')

    def do_disconnect(self, arg):
        'Disconnect a connection: disconnect <name>'
        name = arg.strip()
        if name in self.connections:
            try:
                self.connections[name].close()
            except Exception:
                pass
            del self.connections[name]
            if self.default_conn == name:
                self.default_conn = next(iter(self.connections), None)
            print(f'Disconnected "{name}".')
        else:
            print(f'No such connection: {name}')

    def do_bg_receive(self, arg):
        'Toggle background receive mode: bg_receive'
        if self.bg_receive:
            self._stop_bg.set()
            if self.bg_thread:
                self.bg_thread.join()
            self.bg_receive = False
            print('Background receive stopped.')
        else:
            if not self.default_conn or self.default_conn not in self.connections:
                print('No default connection. Use connect or select.')
                return
            self._stop_bg.clear()
            self.bg_thread = threading.Thread(target=self._bg_receive_loop, daemon=True)
            self.bg_thread.start()
            self.bg_receive = True
            print('Background receive started.')

    def _bg_receive_loop(self):
        s = self.connections[self.default_conn]
        while not self._stop_bg.is_set():
            try:
                s.settimeout(0.5)
                data = s.recv(BUFFER_SIZE)
                if data:
                    msg = data.decode("utf-8", errors="replace")
                    self._add_history('recv', msg)
                    print(f'\n[BG RECEIVED]: {msg}\n{self.prompt}', end="", flush=True)
                else:
                    time.sleep(0.1)
            except socket.timeout:
                continue
            except Exception:
                break

    def do_history(self, arg):
        'Show last 10 sent/received messages: history'
        if not self.history:
            print('No message history.')
            return
        for direction, msg in self.history[-self.max_history:]:
            print(f'[{direction}] {msg}')

    def _add_history(self, direction, msg):
        self.history.append((direction, msg))
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def do_quit(self, arg):
        'Quit the interactive CLI: quit'
        if self.bg_receive:
            self._stop_bg.set()
            if self.bg_thread:
                self.bg_thread.join()
        for s in self.connections.values():
            try:
                s.close()
            except Exception:
                pass
        print('Exiting kn-sock interactive CLI.')
        return True

    def do_exit(self, arg):
        'Exit the interactive CLI: exit'
        return self.do_quit(arg)

    def emptyline(self):
        pass

    def do_help(self, arg):
        'Show help for all commands: help'
        super().do_help(arg)

if __name__ == '__main__':
    KnSockInteractiveCLI().cmdloop() 