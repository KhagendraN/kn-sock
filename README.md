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

## 🐳 Docker Usage

The project includes a `Dockerfile` for building a minimal image and a `docker-compose.yml` for orchestrating CLI and test runs. These files are kept up to date with the latest project structure.

### Using Pre-built Docker Image

Run kn-sock CLI directly with Docker:

```bash
# Show help
docker-compose run knsock

# Run specific commands (examples)
docker-compose run knsock tcp-server --port 8080
docker-compose run knsock tcp-client --host localhost --port 8080 --message "Hello Docker!"
```

### Building and Running Tests

```bash
# Build the Docker image (uses Dockerfile)
docker-compose build

# Run all tests (uses docker-compose.yml 'test' service)
docker-compose run test

# Run specific test file
docker-compose run test pytest test/test_tcp_udp_msg.py -v
```

### Using Docker for Development

```bash
# Build the image (uses Dockerfile)
docker build -t knsock:latest .

# Run interactively
docker run -it --rm -v $(pwd):/app knsock:latest bash

# Run CLI commands
docker run --rm --network host knsock:latest tcp-server --port 8080
```

### Docker Compose Services

The `docker-compose.yml` provides two services:

- **knsock**: Main service for running CLI commands
- **test**: Service for running the test suite

---

## 🧹 Code Style & Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to enforce code style and quality. The configuration is in `.pre-commit-config.yaml` and includes hooks for Black, Flake8, mypy, and basic whitespace/EOF checks.

**To install and run pre-commit hooks:**

```bash
pip install pre-commit
pre-commit install  # Set up git hooks
pre-commit run --all-files  # Run on all files
```

This ensures your code is formatted, linted, and type-checked before committing. See `.pre-commit-config.yaml` for details.

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
