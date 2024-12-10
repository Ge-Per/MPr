import socket

HOST = '127.0.0.1'
PORT = 7777

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)  # Allow only ONE client connection at a time
    print(f"Server is running on {HOST}:{PORT}, waiting for a connection...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")

        # Open a file to write the incoming data
        with open('received_file.txt', 'wb') as f:
            while True:
                data = conn.recv(1024)  # Receive up to 1024 bytes at a time
                if not data:  # If no data is received, stop
                    break
                f.write(data)  # Write data to the file

        print("File received and saved as 'received_file.txt'.")
        print("Closing connection...")
