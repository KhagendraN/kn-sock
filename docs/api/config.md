# Configuration & Environment Variables

kn-sock can be configured using CLI arguments, environment variables, or direct Python parameters.  

This page summarizes supported options and recommended practices for customizing runtime behavior.

## CLI Configuration

Most CLI commands support options like `--host`, `--port`, or protocol-specific flags.  
Check `--help` on any command for available options.

**Example:**
```sh
docker-compose run --rm knsock run-tcp-server 9000 --host 0.0.0.0
```

#### Options Table
| Option            | Description                           |
|-------------------|---------------------------------------|
| `--host`          | Host/IP address (if supported)        |
| `--port`          | Port number (if supported)            |
| Environment vars  | e.g., `KNSOCK_LOGLEVEL=DEBUG`        |

## Environment Variables

Set environment variables to adjust logging, debugging, and other behavior globally.

| Variable            | Description                     | Example Value        |
|---------------------|---------------------------------|----------------------|
| KNSOCK_LOGLEVEL     | Python logging level            | DEBUG, INFO          |
| KNSOCK_CONFIG       | Path to a config file (if supported) | ./knsock.cfg   |
| PYTHONUNBUFFERED    | Unbuffered output for Docker logs | 1                |

Set in shell:
```sh
export KNSOCK_LOGLEVEL=DEBUG
docker-compose run --rm knsock run-tcp-server 9000
```

Or in Docker Compose:
```yaml
services:
  knsock:
    environment:
      - KNSOCK_LOGLEVEL=DEBUG
```

## Python API Configuration

Most kn-sock server/client functions accept keyword arguments for customization.

Example:
```python
from kn_sock import start_tcp_server

start_tcp_server(9000, host='0.0.0.0', loglevel='DEBUG')
```

## Sample Config File (Custom Usage)

If your project extends kn-sock, you may use config files in INI, YAML, or JSON format.
Example (knsock.cfg):
```ini
[server]
host = 0.0.0.0
port = 9000
loglevel = INFO
```

Read this file in your own Python wrapper or extend kn-sock’s startup code.

## Best Practices

Prefer CLI flags for per-invocation overrides.

Use environment variables for cross-platform, repeatable setups (especially in Docker).

For complex deployments, use configuration files and parse them at the application level.

## Troubleshooting

| Issue                    | Symptom/Output            | Solution                                    |
|--------------------------|---------------------------|---------------------------------------------|
| Logging not verbose      | No debug output in terminal | Set KNSOCK_LOGLEVEL=DEBUG                |
| Config not applied       | No change despite editing config | Confirm correct syntax and load sequence |
| Docker not picking up env | No effect in container    | Use environment: in Compose, not just export |