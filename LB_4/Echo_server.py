import socket

HOST = '127.0.0.1'
PORT = 7777

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Allow up to 5 connections in the queue
    print(f"Server running on port {PORT}. Waiting for connections...")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)  # Receive up to 1024 bytes
                if not data:
                    print(f"Connection closed by {addr}")
                    break
                print(f"Received: {data.decode('utf-8')}")
                conn.sendall(data)
                print(f"Sent: {data.decode('utf-8')}")
