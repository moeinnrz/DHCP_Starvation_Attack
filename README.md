# DHCP Starvation Attack Script

This Python script is designed to perform a **DHCP Starvation** attack. In this attack, all available IP addresses on the DHCP Server are filled with fake requests to prevent IP allocation to real clients.

![IMGDHCB](https://github.com/user-attachments/assets/262e3b54-541b-435f-8836-977b76c06e5d)

✅ README.md file:

# DHCP Starvation Attack Script

This Python script is designed to perform a **DHCP Starvation** attack. In this attack, all available IP addresses on the DHCP Server are filled with fake requests to prevent IP allocation to real clients.

## 🛠 Prerequisites

To run the script correctly, you need to install the following tools and packages:

- Python 3.x
- [Npcap](https://npcap.com/) (Windows only)
- pip


## 📦 Install dependencies

First, install the required packages using pip:

```bash
pip install -r requirements.txt
```

Contents of the requirements.txt file:
```bash
scapy
colorama
pyfiglet
```

⚠️ If scapy was installed with limited access, it is better to install it as administrator or with sudo.

💻 Installing Npcap on Windows

If you are using Windows, you must first download and install Npcap. It is recommended to enable the "Install Npcap in WinPcap API-compatible Mode" option during installation.

## ⚙️ How to run

Clone the repository:

```bash
[https://github.com/moeinnrz/Smart_Parking_Detection-.git](https://github.com/moeinnrz/DHCP_Starvation_Attack_DHCBreaker.git)
```
📌 Windows

1- Make sure Npcap is installed.

2- Run the terminal as Administrator.

3- Run the script:
```bash
python dhcp_starvation.py
```

🐧 Linux

1- Make sure Python and pip are installed.

2- Install packages:
```bash
sudo pip install -r requirements.txt
```

3- Run the script with root access:
```bash
sudo python3 dhcp_starvation.py
```

## ✨ Script Features

Display a beautiful graphic banner with pyfiglet

List of available network cards

Select a network card of your choice

Send DHCP Discover with a random MAC and hostname

Receive DHCP Offer and send DHCP Request to confirm IP

## ⚠️ Warning

This script is written for training and testing purposes only in laboratory or controlled environments. Using it on public networks or without the consent of the network administrator is illegal and has serious consequences.
