# Troubleshooting & FAQ

Common issues, error messages, and solutions for working with kn-sock in Docker, Codespaces, and local environments.

## General Issues

| Issue                                  | Symptom/Output                                 | Solution/Workaround                           |
|----------------------------------------|-----------------------------------------------|-----------------------------------------------|
| Port already in use                    | `[Errno 98] Address already in use`           | Use a different port, or kill the process     |
| Hostname not found                     | `[Errno -2] Name or service not known`        | Use the container/server IP, not a name       |
| Connection refused                     | `ConnectionRefusedError`                      | Make sure the server is running               |
| Missing dependency (libGL, etc.)       | `ImportError: libGL.so.1...`                  | Install system packages (see below)             |
| Docker network not found               | `Error: network kn-sock_default not found`    | Recreate the network with `docker-compose up` |
| Large file transfer fails              | Partial/incomplete transfer or disconnect     | Check disk space, increase timeouts           |
| No server response (UDP)               | No echo, no data returned                     | UDP is connectionless; check ports/firewalls  |

## Docker-Specific Issues

| Issue                                 | Symptom/Output                      | Solution/Workaround                           |
|---------------------------------------|-------------------------------------|-----------------------------------------------|
| Cannot reach service by name           | Hostname not found                  | Use container IP (see `docker inspect ...`)   |
| GUI/X11 issues (live video/audio)      | No display, blank window            | Use local Python if GUI needed                |
| File permissions (file transfer)       | No file saved or permission denied  | Use directories with write access             |
| Orphan containers/network clutter      | Warnings about orphan containers    | Use `docker-compose down --remove-orphans`    |

## System Dependencies

Some features require system libraries:
- **OpenCV/Video streaming:**  
  `libGL.so.1`, `libgthread-2.0.so.0`, and other dependencies
- **Audio streaming:**  
  `libportaudio2`, `alsa-utils`, etc.

On Debian/Ubuntu-based systems, you may need:
```sh
apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libportaudio2 \
    portaudio19-dev \
    libasound2 \
    ffmpeg \
    gcc
```

### How to Find Container IP
```sh
docker ps  # Find your container ID
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_id>
```
Use this IP for client commands in Docker Compose.

## FAQ

**Q: Why can't I use the service name as the host in Docker Compose?**  
A: In `docker-compose run`, the new container is not on the same network by default. Use the server container’s IP.

**Q: Why are my CLI commands hanging or failing?**  
A: Confirm the server is running, port is correct, and network is open.

**Q: Why do I see import errors for system libraries?**  
A: Install missing system packages, or use the provided Dockerfile.

**Q: How can I test two endpoints at once?**  
A: Run each service (server/client) in its own terminal. For automation, write a shell script or use pytest with subprocess calls.

**Q: Where do I file bugs or ask for help?**  
A: Open an issue on GitHub.