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
## See Also

- **[CLI Guide](cli.md)** - Complete CLI reference
- **[Getting Started](getting-started.md)** - Basic setup without Docker
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[Examples](examples.md)** - Real-world usage examples
