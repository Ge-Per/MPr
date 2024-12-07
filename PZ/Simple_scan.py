import socket


def scan_ports(ip, start_port, end_port):
    print(f"Scanning ports {start_port} to {end_port} on {ip}...")
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))  # 0 if open
            if result == 0:
                print(f"Port {port} is open")


if __name__ == "__main__":
    target_ip = input("Enter target IP: ")
    #start = int(input("Enter start port: "))
    #end = int(input("Enter end port: "))

    scan_ports(target_ip, 1, 1000)
