# TCP Utilities

kn-sock provides both CLI and Python APIs for working with TCP servers and clients.

=== "CLI"

    ### Run a TCP Echo Server

    | Command | Description |
    |---|---|
    | `run-tcp-server <port>` | Start a TCP echo server |

    ```sh
    docker-compose run --rm knsock run-tcp-server 8080
    # Or: knsock run-tcp-server 8080
    ```

    !!! tip "Find server IP in Docker"
        ```sh
        docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container>
        ```

=== "Python API"

    ### Quickstart

    ```python
    from kn_sock import send_tcp_message
    send_tcp_message("127.0.0.1", 8080, "Hello TCP")
    ```

    ### Reference

    ::: kn_sock.tcp.start_tcp_server
        options:
          heading_level: 3
          members_order: source
          filters: ["!^_"]
          show_source: false
