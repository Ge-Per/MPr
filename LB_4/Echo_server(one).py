import socket

HOST = '127.0.0.1'
PORT = 7777

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)  # Allow only ONE client connection at a time
    print(f"Server is running on {HOST}:{PORT}, waiting for a connection...")

    # Accept a single connection
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")

        data = conn.recv(1024)  # Receive up to 1024 bytes
        if data:
            print(f"Received: {data.decode('utf-8')}")
            response = f"[ECHO] {data.decode('utf-8')}"
            conn.sendall(response.encode('utf-8'))  # Send back the response
            print(f"Sent: {response}")

        print("Closing connection...")
