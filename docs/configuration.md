# Configuration

Configuration options for customizing kn-sock behavior.

## Configuration Files

### YAML Configuration

Create `config.yaml`:

```yaml
network:
  host: "0.0.0.0"
  port: 8080
  timeout: 30

ssl:
  cert_file: "server.crt"
  key_file: "server.key"
  ca_file: "ca.crt"

logging:
  level: "INFO"
```

### JSON Configuration

Create `config.json`:

```json
{
  "network": {
    "host": "0.0.0.0",
    "port": 8080,
    "timeout": 30
  },
  "ssl": {
    "cert_file": "server.crt", 
    "key_file": "server.key"
  }
}
```

## Using Configuration

```python
from kn_sock.config import load_config, get_config

# Load configuration file
load_config("config.yaml")

# Get configuration values
host = get_config("network.host", "localhost")
port = get_config("network.port", 8080)
```

## Environment Variables

Override configuration with environment variables:

```bash
export KN_SOCK_HOST="127.0.0.1"
export KN_SOCK_PORT="9000"
export KN_SOCK_SSL_VERIFY="false"
```

## Common Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `host` | Server bind address | "0.0.0.0" |
| `port` | Server port | 8080 |
| `timeout` | Connection timeout | 30 seconds |
| `buffer_size` | Socket buffer size | 4096 bytes |
| `ssl.verify` | SSL certificate verification | True |

## Configuration Hierarchy

Settings are applied in order:
1. Built-in defaults
2. Configuration file
3. Environment variables
4. Runtime parameters
