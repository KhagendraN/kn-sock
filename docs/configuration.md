# Configuration Guide

kn-sock provides flexible configuration options to customize behavior for different environments and use cases.

## Overview

Configuration in kn-sock can be managed through:
- **Environment variables**: For deployment-specific settings
- **Configuration files**: For complex, structured configuration
- **Runtime parameters**: For dynamic configuration changes
- **Global defaults**: Built-in sensible defaults for all features

## Configuration Methods

### 1. Environment Variables

Set environment variables to configure kn-sock behavior:

```bash
# Basic networking
export KN_SOCK_DEFAULT_HOST="0.0.0.0"
export KN_SOCK_DEFAULT_PORT="8080"
export KN_SOCK_TIMEOUT="30"

# Security settings
export KN_SOCK_SSL_VERIFY="true"
export KN_SOCK_SSL_CERT_PATH="/path/to/cert.pem"
export KN_SOCK_SSL_KEY_PATH="/path/to/key.pem"

# Performance tuning
export KN_SOCK_BUFFER_SIZE="8192"
export KN_SOCK_MAX_CONNECTIONS="100"
export KN_SOCK_THREAD_POOL_SIZE="10"

# Logging
export KN_SOCK_LOG_LEVEL="INFO"
export KN_SOCK_LOG_FILE="/var/log/kn-sock.log"

# Run your application
python your_app.py
```

### 2. Configuration Files

Create a configuration file for structured settings:

**config.yaml:**
```yaml
# Network Configuration
network:
  default_host: "0.0.0.0"
  default_port: 8080
  timeout: 30
  buffer_size: 8192
  max_connections: 100
  keep_alive: true
  tcp_nodelay: true

# Security Configuration
security:
  ssl:
    enabled: true
    cert_file: "/path/to/cert.pem"
    key_file: "/path/to/key.pem"
    ca_file: "/path/to/ca.pem"
    verify_mode: "CERT_REQUIRED"
  authentication:
    enabled: true
    secret_key: "your-secret-key"
    token_expiry: 3600

# Performance Configuration
performance:
  thread_pool_size: 10
  connection_pool_size: 20
  async_workers: 4
  compression:
    enabled: true
    algorithm: "gzip"
    level: 6

# Logging Configuration
logging:
  level: "INFO"
  file: "/var/log/kn-sock.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  max_size: "10MB"
  backup_count: 5

# Protocol-specific Configuration
protocols:
  tcp:
    keepalive: true
    keepalive_idle: 7200
    keepalive_interval: 75
    keepalive_probes: 9
  
  udp:
    multicast_ttl: 1
    broadcast: false
  
  websocket:
    ping_interval: 20
    ping_timeout: 10
    max_message_size: "1MB"
  
  http:
    user_agent: "kn-sock/1.0"
    timeout: 30
    max_redirects: 5

# Feature-specific Configuration
features:
  file_transfer:
    chunk_size: 64KB
    progress_callback: true
    checksum_verification: true
  
  live_streaming:
    buffer_size: 1MB
    quality_levels: [240, 480, 720, 1080]
    adaptive_bitrate: true
  
  pubsub:
    max_subscribers: 1000
    message_history: 100
    persistence: true
  
  rpc:
    timeout: 30
    retry_attempts: 3
    load_balancing: "round_robin"
```

**Using the configuration file:**

```python
from kn_sock.config import load_config

# Load configuration
config = load_config("config.yaml")

# Use configured settings
from kn_sock import start_tcp_server

start_tcp_server(
    port=config.network.default_port,
    host=config.network.default_host,
    timeout=config.network.timeout
)
```

### 3. Runtime Configuration

Configure settings programmatically at runtime:

```python
from kn_sock.config import Config

# Create configuration instance
config = Config()

# Set network configuration
config.set_network_config(
    default_host="localhost",
    default_port=9000,
    timeout=60,
    buffer_size=16384
)

# Set SSL configuration
config.set_ssl_config(
    cert_file="server.crt",
    key_file="server.key",
    verify_mode="CERT_OPTIONAL"
)

# Set performance configuration
config.set_performance_config(
    thread_pool_size=20,
    connection_pool_size=50,
    compression_enabled=True
)

# Apply configuration globally
config.apply_global()

# Now all kn-sock operations will use these settings
from kn_sock import start_tcp_server
start_tcp_server(8080, handler)  # Uses configured settings
```

## Configuration Categories

### Network Configuration

Control fundamental networking behavior:

```python
from kn_sock.config import NetworkConfig

network_config = NetworkConfig(
    # Basic settings
    default_host="0.0.0.0",
    default_port=8080,
    timeout=30,
    
    # Buffer and connection limits
    buffer_size=8192,
    max_connections=100,
    backlog=128,
    
    # TCP-specific options
    keep_alive=True,
    tcp_nodelay=True,
    socket_reuse=True,
    
    # Retry and timeout settings
    connect_timeout=10,
    read_timeout=30,
    write_timeout=30,
    retry_attempts=3,
    retry_delay=1.0
)
```

**Environment Variables:**
- `KN_SOCK_DEFAULT_HOST`: Default host for servers
- `KN_SOCK_DEFAULT_PORT`: Default port for servers
- `KN_SOCK_TIMEOUT`: Default timeout for operations
- `KN_SOCK_BUFFER_SIZE`: Socket buffer size
- `KN_SOCK_MAX_CONNECTIONS`: Maximum concurrent connections

### Security Configuration

Configure SSL/TLS and authentication:

```python
from kn_sock.config import SecurityConfig

security_config = SecurityConfig(
    # SSL/TLS settings
    ssl_enabled=True,
    ssl_cert_file="/path/to/server.crt",
    ssl_key_file="/path/to/server.key",
    ssl_ca_file="/path/to/ca.crt",
    ssl_verify_mode="CERT_REQUIRED",  # CERT_NONE, CERT_OPTIONAL, CERT_REQUIRED
    ssl_check_hostname=True,
    ssl_ciphers="HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA",
    
    # Authentication settings
    auth_enabled=True,
    auth_secret_key="your-secret-key",
    auth_algorithm="HS256",
    auth_token_expiry=3600,
    
    # Rate limiting
    rate_limit_enabled=True,
    rate_limit_requests=100,
    rate_limit_window=60,
    
    # IP filtering
    allowed_ips=["192.168.1.0/24", "10.0.0.0/8"],
    blocked_ips=["192.168.1.100"]
)
```

**Environment Variables:**
- `KN_SOCK_SSL_CERT_PATH`: Path to SSL certificate
- `KN_SOCK_SSL_KEY_PATH`: Path to SSL private key
- `KN_SOCK_SSL_VERIFY`: SSL verification mode
- `KN_SOCK_AUTH_SECRET`: Authentication secret key

### Performance Configuration

Optimize performance for your use case:

```python
from kn_sock.config import PerformanceConfig

performance_config = PerformanceConfig(
    # Threading configuration
    thread_pool_size=10,
    thread_pool_max_size=50,
    thread_timeout=300,
    
    # Connection pooling
    connection_pool_size=20,
    connection_pool_max_size=100,
    connection_idle_timeout=300,
    
    # Async configuration
    async_workers=4,
    async_queue_size=1000,
    
    # Compression settings
    compression_enabled=True,
    compression_algorithm="gzip",  # gzip, deflate, brotli
    compression_level=6,
    compression_threshold=1024,
    
    # Caching
    cache_enabled=True,
    cache_size=1000,
    cache_ttl=300,
    
    # Memory management
    max_memory_usage="512MB",
    gc_threshold=10000
)
```

**Environment Variables:**
- `KN_SOCK_THREAD_POOL_SIZE`: Thread pool size
- `KN_SOCK_COMPRESSION`: Enable/disable compression
- `KN_SOCK_CACHE_SIZE`: Cache size limit

### Logging Configuration

Control logging behavior:

```python
from kn_sock.config import LoggingConfig

logging_config = LoggingConfig(
    # Basic logging settings
    level="INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    
    # File logging
    file_enabled=True,
    file_path="/var/log/kn-sock.log",
    file_max_size="10MB",
    file_backup_count=5,
    
    # Console logging
    console_enabled=True,
    console_colored=True,
    
    # Structured logging
    structured=True,
    json_format=False,
    
    # Performance logging
    performance_logging=True,
    slow_query_threshold=1.0,
    
    # Security logging
    security_events=True,
    audit_trail=True
)
```

**Environment Variables:**
- `KN_SOCK_LOG_LEVEL`: Logging level
- `KN_SOCK_LOG_FILE`: Log file path
- `KN_SOCK_LOG_FORMAT`: Log message format

## Protocol-Specific Configuration

### TCP Configuration

```python
from kn_sock.config import TCPConfig

tcp_config = TCPConfig(
    # Connection settings
    keepalive=True,
    keepalive_idle=7200,      # Seconds before sending keepalive probes
    keepalive_interval=75,    # Interval between keepalive probes
    keepalive_probes=9,       # Number of keepalive probes
    
    # Socket options
    tcp_nodelay=True,         # Disable Nagle's algorithm
    socket_reuse=True,        # Enable SO_REUSEADDR
    
    # Buffer settings
    send_buffer_size=65536,
    recv_buffer_size=65536,
    
    # Timeout settings
    connect_timeout=10,
    send_timeout=30,
    recv_timeout=30
)
```

### WebSocket Configuration

```python
from kn_sock.config import WebSocketConfig

websocket_config = WebSocketConfig(
    # Connection management
    ping_interval=20,         # Seconds between ping frames
    ping_timeout=10,          # Timeout waiting for pong
    close_timeout=10,         # Timeout for close handshake
    
    # Message limits
    max_message_size="1MB",
    max_frame_size="64KB",
    max_queue_size=100,
    
    # Compression
    per_message_deflate=True,
    compression_level=6,
    
    # Subprotocols
    subprotocols=["chat", "echo"],
    
    # Headers
    extra_headers={
        "Server": "kn-sock/1.0"
    }
)
```

### RPC Configuration

```python
from kn_sock.config import RPCConfig

rpc_config = RPCConfig(
    # Timeout settings
    call_timeout=30,
    connect_timeout=10,
    
    # Retry configuration
    retry_attempts=3,
    retry_delay=1.0,
    retry_backoff="exponential",  # linear, exponential
    
    # Load balancing
    load_balancing="round_robin",  # round_robin, random, least_connections
    health_check_interval=30,
    
    # Serialization
    serialization="json",     # json, pickle, protobuf
    compression=True,
    
    # Authentication
    auth_required=False,
    auth_timeout=60,
    
    # Middleware
    middleware_enabled=True,
    request_logging=True,
    performance_monitoring=True
)
```

## Environment-Specific Configuration

### Development Configuration

```yaml
# development.yaml
network:
  default_host: "127.0.0.1"
  default_port: 8080

security:
  ssl:
    enabled: false
  authentication:
    enabled: false

logging:
  level: "DEBUG"
  console_enabled: true
  file_enabled: false

performance:
  thread_pool_size: 2
  compression:
    enabled: false
```

### Production Configuration

```yaml
# production.yaml
network:
  default_host: "0.0.0.0"
  default_port: 8080
  max_connections: 1000

security:
  ssl:
    enabled: true
    cert_file: "/etc/ssl/certs/server.crt"
    key_file: "/etc/ssl/private/server.key"
    verify_mode: "CERT_REQUIRED"
  authentication:
    enabled: true
    secret_key: "${AUTH_SECRET_KEY}"

logging:
  level: "INFO"
  file_enabled: true
  file_path: "/var/log/kn-sock.log"
  structured: true

performance:
  thread_pool_size: 20
  connection_pool_size: 100
  compression:
    enabled: true
    level: 6
```

### Testing Configuration

```yaml
# testing.yaml
network:
  default_host: "127.0.0.1"
  timeout: 5

security:
  ssl:
    enabled: false
  authentication:
    enabled: false

logging:
  level: "WARNING"
  console_enabled: false
  file_enabled: false

performance:
  thread_pool_size: 1
  compression:
    enabled: false

features:
  file_transfer:
    chunk_size: 1KB
  live_streaming:
    buffer_size: 64KB
```

## Configuration Loading

### Loading Order

kn-sock loads configuration in the following order (later sources override earlier ones):

1. Built-in defaults
2. System configuration file (`/etc/kn-sock/config.yaml`)
3. User configuration file (`~/.kn-sock/config.yaml`)
4. Local configuration file (`./kn-sock.yaml`)
5. Environment variables
6. Runtime configuration
7. Function/method parameters

### Configuration File Discovery

```python
from kn_sock.config import load_config

# Automatic discovery (searches standard locations)
config = load_config()

# Explicit file path
config = load_config("/path/to/config.yaml")

# Multiple files (merged in order)
config = load_config([
    "/etc/kn-sock/default.yaml",
    "/etc/kn-sock/production.yaml",
    "./local-overrides.yaml"
])

# With environment-based selection
import os
env = os.getenv("ENVIRONMENT", "development")
config = load_config(f"config/{env}.yaml")
```

### Validation and Defaults

```python
from kn_sock.config import Config, ValidationError

try:
    config = Config.from_file("config.yaml")
    
    # Validate configuration
    config.validate()
    
    # Get with defaults
    port = config.get("network.port", default=8080)
    ssl_enabled = config.get("security.ssl.enabled", default=False)
    
except ValidationError as e:
    print(f"Configuration error: {e}")
    # Handle validation errors
```

## Configuration Best Practices

### 1. Use Environment Variables for Secrets

```yaml
# config.yaml - Never put secrets directly in config files
security:
  authentication:
    secret_key: "${AUTH_SECRET_KEY}"
  ssl:
    cert_file: "${SSL_CERT_PATH}"
    key_file: "${SSL_KEY_PATH}"
```

```bash
# Set environment variables
export AUTH_SECRET_KEY="your-secret-key"
export SSL_CERT_PATH="/path/to/cert.pem"
export SSL_KEY_PATH="/path/to/key.pem"
```

### 2. Environment-Specific Configurations

```python
import os
from kn_sock.config import load_config

# Load environment-specific configuration
environment = os.getenv("ENVIRONMENT", "development")
config_file = f"config/{environment}.yaml"
config = load_config(config_file)
```

### 3. Configuration Validation

```python
from kn_sock.config import Config, ConfigSchema
from marshmallow import fields

class NetworkConfigSchema(ConfigSchema):
    host = fields.Str(required=True, validate=lambda x: len(x) > 0)
    port = fields.Int(required=True, validate=lambda x: 1 <= x <= 65535)
    timeout = fields.Int(validate=lambda x: x > 0)

# Validate configuration against schema
config = Config.from_file("config.yaml")
schema = NetworkConfigSchema()
errors = schema.validate(config.network)

if errors:
    print(f"Configuration errors: {errors}")
```

### 4. Configuration Monitoring

```python
import threading
import time
from kn_sock.config import Config

class ConfigMonitor:
    def __init__(self, config_file, reload_callback=None):
        self.config_file = config_file
        self.reload_callback = reload_callback
        self.last_modified = os.path.getmtime(config_file)
        self.monitoring = True
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor, daemon=True)
        self.monitor_thread.start()
    
    def _monitor(self):
        while self.monitoring:
            try:
                current_modified = os.path.getmtime(self.config_file)
                if current_modified > self.last_modified:
                    print("Configuration file changed, reloading...")
                    new_config = Config.from_file(self.config_file)
                    
                    if self.reload_callback:
                        self.reload_callback(new_config)
                    
                    self.last_modified = current_modified
                    
            except Exception as e:
                print(f"Error monitoring config file: {e}")
            
            time.sleep(1)  # Check every second

# Usage
def on_config_reload(new_config):
    print("Configuration reloaded!")
    # Update application settings

monitor = ConfigMonitor("config.yaml", on_config_reload)
```

### 5. Configuration Documentation

Always document your configuration options:

```yaml
# config.yaml
# Network Configuration
network:
  # Host to bind servers to (default: 0.0.0.0)
  default_host: "0.0.0.0"
  
  # Default port for servers (default: 8080)
  default_port: 8080
  
  # Connection timeout in seconds (default: 30)
  timeout: 30
  
  # Maximum concurrent connections (default: 100)
  max_connections: 100

# Security Configuration
security:
  ssl:
    # Enable SSL/TLS encryption (default: false)
    enabled: true
    
    # Path to SSL certificate file (required if SSL enabled)
    cert_file: "/path/to/cert.pem"
    
    # Path to SSL private key file (required if SSL enabled)
    key_file: "/path/to/key.pem"
```

## Troubleshooting Configuration

### Common Configuration Issues

#### 1. File Not Found
```python
try:
    config = load_config("config.yaml")
except FileNotFoundError:
    print("Configuration file not found, using defaults")
    config = Config.default()
```

#### 2. Invalid Configuration Values
```python
try:
    config = load_config("config.yaml")
    config.validate()
except ValidationError as e:
    print(f"Invalid configuration: {e}")
    # Fix configuration or exit
```

#### 3. Environment Variable Issues
```bash
# Check if environment variables are set
env | grep KN_SOCK

# Debug environment variable loading
export KN_SOCK_DEBUG=true
python your_app.py
```

#### 4. Permission Issues
```bash
# Ensure configuration files are readable
chmod 644 config.yaml

# Ensure SSL files have correct permissions
chmod 600 /path/to/server.key
chmod 644 /path/to/server.crt
```

### Configuration Debugging

```python
from kn_sock.config import Config

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Load configuration with debug info
config = Config.from_file("config.yaml", debug=True)

# Print effective configuration
print("Effective configuration:")
config.dump()

# Check configuration sources
print("Configuration sources:")
for source in config.sources:
    print(f"  - {source}")
```

## See Also

- **[Getting Started](getting-started.md)** - Basic setup and configuration
- **[Docker Guide](docker.md)** - Docker-specific configuration
- **[Security Guide](security.md)** - Security configuration best practices
- **[Performance Guide](performance.md)** - Performance tuning configuration
- **[Troubleshooting](troubleshooting.md)** - Common configuration issues
