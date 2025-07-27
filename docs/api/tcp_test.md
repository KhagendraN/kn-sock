# Tabs Demo

## Basic Tabs

=== "Python"

    ```python
    def greet():
        print("Hello from Python!")
    ```

=== "JavaScript"

    ```javascript
    function greet() {
        console.log("Hello from JavaScript!");
    }
    ```

=== "Shell"

    ```bash
    echo "Hello from Bash"
    ```

## Tabs with Content

=== "Overview"

    This section gives you a high-level overview of the system.

=== "Details"

    Here's where we break it down into components and logic.

=== "More Info"

    Links, references, and related topics go here.


## Sending a TCP Message

=== "CLI"

    ```sh
    docker-compose run --rm knsock send-tcp 172.18.0.2 8080 "Hello TCP"
    ```

    Output:
    ```
    [TCP] Server response: Echo: Hello TCP
    ```

=== "Python"

    ```python
    from kn_sock import send_tcp_message
    send_tcp_message('127.0.0.1', 8080, "Hello TCP")
    ```

    Output:
    ```
    [TCP] Server response: Echo: Hello TCP
    ```
