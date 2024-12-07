from scapy.all import *


def syn_scan(target, ports):
    print(f"SYN scan on {target} with ports {ports}")
    sport = RandShort()
    for port in ports:
        pkt = sr1(IP(dst=target)/TCP(sport=sport, dport=port, flags="S"), timeout=1, verbose=0)
        if pkt != None:
            if pkt.haslayer(TCP):
                if pkt[TCP].flags == 20:
                    continue
                elif pkt[TCP].flags == 18:
                    print(f"{port} | Open")
                else:
                    print(f"{port} | TCP packet resp / filtered")
            elif pkt.haslayer(ICMP):
                print(f"{port} | ICMP resp / filtered")
            else:
                print(f"{port} | Unknown resp")
                print(pkt.summary())
        else:
            print(f"{port} | Unanswered")


def xmas_scan(target, ports):
    print(f"Xmas scan on {target} with ports {ports}")
    sport = RandShort()
    for port in ports:
        pkt = sr1(IP(dst=target)/TCP(sport=sport, dport=port, flags="FPU"), timeout=1, verbose=0)
        if pkt != None:
            if pkt.haslayer(TCP):
                if pkt[TCP].flags == 20:
                    continue
                else:
                    print(f"{port} | TCP flag {pkt[TCP].flag}")
            elif pkt.haslayer(ICMP):
                print(f"{port} | ICMP resp / filtered")
            else:
                print(f"{port} | Unknown resp")
                print(pkt.summary())
        else:
            print(f"{port} | Open / filtered")


def menu():
    print("\nSelect scan type:")
    print("1. SYN Scan")
    print("2. Xmas Scan")
    print("3. Exit")


def main():
    target = input("Enter target IP: ")
    ports = range(1, 1000)

    while True:
        menu()
        choice = input("Choose an option (1-3): ")

        if choice == "1":
            syn_scan(target, ports)
        elif choice == "2":
            xmas_scan(target, ports)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
