# Using the CLI

The knsock command-line interface provides quick access to all TCP, UDP, and WebSocket tools.
It's built using Typer, giving it a structured syntax and automatic help output.

Run all commands using either knsock (if installed via pip) or via Docker.

## CLI Structure

```css
knsock [PROTOCOL] [COMMAND] [OPTIONS]
```

## Supported Protocols

- **tcp** – Synchronous and multithreaded TCP servers and clients
- **udp** – Synchronous UDP echo server and datagram sender
- **websocket** – WebSocket echo server and client message sender

## Top-Level Help

```bash
knsock --help
```

Output:

```vbnet
Usage: knsock [OPTIONS] COMMAND [ARGS]...

  knsock: Network testing CLI for TCP, UDP, and WebSocket.

Options:
  --help  Show this message and exit.

Commands:
  tcp        TCP servers and clients
  udp        UDP servers and clients
  websocket  WebSocket servers and clients
```

## Run from Docker

```bash
docker-compose run --rm knsock --help
```

## Use Case

Use the CLI when you need:

- Quick network diagnostics
- Shell scripting or automation
- Rapid testing without writing Python code
- Consistent interface across protocols

## Example

Start a TCP echo server:

```bash
knsock tcp run-server 9000
```

Send a message:

```bash
knsock tcp send localhost 9000 "Hello CLI"
```

## Related Pages

- [TCP CLI](../tcp/cli.md)
- [UDP CLI](../udp/cli.md)
- [WebSocket CLI](../websocket/cli.md)