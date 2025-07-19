from kn_sock import send_tcp_message

while True:
    message = input("Enter your message: ")
    send_tcp_message("localhost", 8080, message)
