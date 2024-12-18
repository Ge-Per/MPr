import socket
from tqdm import tqdm  # for Pg-bar

def scan_ports(ip, start_port, end_port):
    print(f"Scanning ports {start_port} to {end_port} on {ip}...")
    for port in tqdm(range(start_port, end_port + 1), desc="Scanning"):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))  # 0 if open
            if result == 0:
                print(" < is open")

if __name__ == "__main__":
    target_ip = input("Enter target IP or domain: ")
    scan_ports(target_ip, 1, 1000)
