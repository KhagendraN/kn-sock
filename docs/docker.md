# Docker Guide

This guide covers how to use kn-sock with Docker for development, testing, and deployment.

## Overview

kn-sock provides Docker support through:
- Pre-built Docker images for running CLI commands
- Docker Compose configuration for easy development
- Containerized test environment
- Production-ready deployment options

## Quick Start

### Using Docker Compose

The easiest way to get started with kn-sock in Docker:

```bash
# Show CLI help
docker-compose run knsock --help

# Start a TCP server
docker-compose run knsock tcp-server --port 8080

# Send a message from another terminal
docker-compose run knsock tcp-client --host localhost --port 8080 --message "Hello Docker!"
```

### Running Tests

```bash
# Run all tests
docker-compose run test

# Run specific test files
docker-compose run test pytest test/test_tcp_udp_msg.py -v

# Run tests with coverage
docker-compose run test pytest --cov=kn_sock test/
```

## Docker Compose Configuration

The `docker-compose.yml` provides two main services:

### knsock Service

```yaml
knsock:
  build: .
  image: knsock:latest
  command: ["--help"]
  volumes:
    - .:/app
```

**Usage:**
- Runs kn-sock CLI commands
- Mounts current directory for development
- Uses host networking for socket operations

### test Service

```yaml
test:
  build: .
  image: knsock:latest
  command: ["pytest", "test/"]
  volumes:
    - .:/app
```

**Usage:**
- Runs the complete test suite
- Isolated testing environment
- Same image as main service for consistency

## Manual Docker Usage

### Building the Image

```bash
# Build the Docker image
docker build -t knsock:latest .

# Build with specific tag
docker build -t knsock:1.0.0 .
```

### Running CLI Commands

```bash
# Show help
docker run --rm knsock:latest --help

# Start a TCP server (requires host networking)
docker run --rm --network host knsock:latest tcp-server --port 8080

# Send a TCP message
docker run --rm --network host knsock:latest tcp-client --host localhost --port 8080 --message "Hello"
```

### Interactive Development

```bash
# Run interactive shell for development
docker run -it --rm -v $(pwd):/app knsock:latest bash

# Inside container, you can run:
# python -m kn_sock.cli --help
# pytest test/
# python examples/tcp_server.py
```

## Production Deployment

### Multi-Stage Build (Recommended)

Create a production Dockerfile:

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
EXPOSE 8080
ENTRYPOINT ["python", "-m", "kn_sock.cli"]
```

### Docker Compose for Production

```yaml
version: '3.8'
services:
  tcp-server:
    build: .
    image: knsock:latest
    command: ["tcp-server", "--port", "8080", "--host", "0.0.0.0"]
    ports:
      - "8080:8080"
    restart: unless-stopped
    
  udp-server:
    build: .
    image: knsock:latest
    command: ["udp-server", "--port", "8081", "--host", "0.0.0.0"]
    ports:
      - "8081:8081/udp"
    restart: unless-stopped
```

## Networking Considerations

### Host Networking

For development and testing, use host networking:

```bash
docker run --network host knsock:latest tcp-server --port 8080
```

**Pros:**
- Simple configuration
- Direct access to host ports
- No port mapping required

**Cons:**
- Less isolation
- Not suitable for production clusters

### Bridge Networking (Recommended for Production)

```bash
# Run with explicit port mapping
docker run -p 8080:8080 knsock:latest tcp-server --port 8080 --host 0.0.0.0
```

**Pros:**
- Better isolation
- Explicit port control
- Works in orchestrated environments

**Cons:**
- Requires port mapping configuration

## Development Workflow

### 1. Code Changes

Make changes to your code, then rebuild:

```bash
docker-compose build
```

### 2. Testing

Run tests to validate changes:

```bash
docker-compose run test
```

### 3. Manual Testing

Test specific functionality:

```bash
# Terminal 1: Start server
docker-compose run knsock tcp-server --port 8080

# Terminal 2: Test client
docker-compose run knsock tcp-client --host localhost --port 8080 --message "Test"
```

## Advanced Usage

### Custom Entrypoint

Override the default entrypoint for custom applications:

```bash
# Run your own application
docker run --rm -v $(pwd):/app --entrypoint python knsock:latest examples/tcp_server.py
```

### Environment Variables

Set environment variables for configuration:

```bash
docker run --rm \
  -e KN_SOCK_DEBUG=1 \
  -e KN_SOCK_LOG_LEVEL=DEBUG \
  knsock:latest tcp-server --port 8080
```

### Volume Mounts

Mount specific directories for file operations:

```bash
# Mount data directory for file transfer
docker run --rm \
  -v $(pwd)/data:/app/data \
  --network host \
  knsock:latest file-server --port 8080 --directory /app/data
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
docker run --rm --network host nicolaka/netshoot netstat -tuln | grep 8080

# Use a different port
docker-compose run knsock tcp-server --port 8081
```

### Permission Issues

```bash
# Run with specific user
docker run --rm --user $(id -u):$(id -g) -v $(pwd):/app knsock:latest --help
```

### Container Won't Start

```bash
# Check container logs
docker-compose logs knsock

# Run with debug output
docker-compose run knsock --debug tcp-server --port 8080
```

### Network Connectivity

```bash
# Test network connectivity
docker run --rm --network host nicolaka/netshoot ping host.docker.internal

# Check if ports are accessible
docker run --rm --network host nicolaka/netshoot telnet localhost 8080
```

## Best Practices

### 1. Use .dockerignore

Create `.dockerignore` to exclude unnecessary files:

```
__pycache__/
*.pyc
.git/
.pytest_cache/
site/
build/
*.egg-info/
.coverage
htmlcov/
```

### 2. Multi-stage Builds

Use multi-stage builds for smaller production images:

```dockerfile
FROM python:3.11-slim as dependencies
RUN pip install kn-sock

FROM python:3.11-slim
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
```

### 3. Health Checks

Add health checks for production deployments:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import socket; s=socket.socket(); s.connect(('localhost', 8080)); s.close()" || exit 1
```

### 4. Security

- Run as non-root user in production
- Use specific image tags instead of `latest`
- Scan images for vulnerabilities
- Use secrets management for sensitive data

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Docker Build and Test
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker-compose build
      - name: Run tests
        run: docker-compose run test
      - name: Test CLI
        run: docker-compose run knsock --help
```

### GitLab CI Example

```yaml
test:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker-compose build
    - docker-compose run test
```

## See Also

- **[CLI Guide](cli.md)** - Complete CLI reference
- **[Getting Started](getting-started.md)** - Basic setup without Docker
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[Examples](examples.md)** - Real-world usage examples
