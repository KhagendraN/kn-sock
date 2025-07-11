<p align="center">
  <img src="Assets/kn-sock_logo.png" alt="kn-sock logo" width="128"/>
</p>

# kn-sock

![PyPI version](https://img.shields.io/pypi/v/kn-sock)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/kn-sock)](https://pypi.org/project/kn-sock/)
[![GitHub Stars](https://img.shields.io/github/stars/KhagendraN/kn-sock?style=social)](https://github.com/KhagendraN/kn-sock/stargazers)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://kn-sock.khagendraneupane.com.np)

A simplified socket programming toolkit for Python.

---

## 🚀 Features

- TCP/UDP Messaging (sync and async)
- JSON over sockets
- File transfer over TCP
- Threaded server support
- CLI for quick socket actions
- Decorators and utility functions

---

## 💡 Use Cases

- Build custom TCP/UDP servers quickly  
- Transfer files between machines  
- Send structured (JSON) data across a network  
- Stream live video and audio to multiple clients (via Python or CLI)  
- Share or execute code snippets over a network  
- Create automated socket-based test environments  
- Use CLI for local or remote debugging and diagnostics  

---

## 📦 Installation

```bash
pip install kn-sock
```

---

## 🔧 Quick Example

```python
from kn_sock import send_tcp_message

send_tcp_message("localhost", 8080, "Hello, World!")
```

---

## 📚 Documentation

### Full documentation is available at
- [kn-sock official site](https://kn-sock.khagendraneupane.com.np)
- [Github documentation](https://github.com/KhagendraN/kn-sock/blob/main/docs/index.md)


---

## 🤝 Contributing

Have ideas or found bugs? Open an issue or submit a pull request!

If you're new:

- See the contributing [guide](CONTRIBUTING.md)
- Or just start with a ⭐ star :)

---

## 🧾 License

This project is licensed under the MIT [License](LICENSE).
