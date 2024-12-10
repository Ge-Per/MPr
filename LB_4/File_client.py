import socket

HOST = '127.0.0.1'
PORT = 7777

file_path = input("Enter the path of the file to send: ")

with open(file_path, 'rb') as f:
    file_data = f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    client_socket.sendall(file_data)

    print(f"File '{file_path}' sent to server.")
