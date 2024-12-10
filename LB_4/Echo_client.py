import socket

HOST = '127.0.0.1'
PORT = 7777

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    try:
        message = input("Enter message to send: ")
        client_socket.sendall(message.encode('utf-8'))
        data = client_socket.recv(1024)
        print(f"Server response: {data.decode('utf-8')}")
    except KeyboardInterrupt:
        print("\nClient interrupted. Exiting.")
