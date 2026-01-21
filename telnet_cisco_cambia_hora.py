#!/usr/bin/python
# @author [Mauricio Lange]
# @email [mauriciolangea@yahoo.com]
# @create date 2025-04-01 15:00
# @modify date 2026-01-21 15:00
# @desc [Automation - Configura Servidor NTP y Zona Horaria a Horario Verano/Invierno en Chile]
# UTC -3 = Verano
# UTC -4 = Invierno

import getpass
import sys
import time
import socket
import telnetlib

TZ_OFFSET  = "UTC -3 0"
HOSTS_FILE = "hosts"
NTP_SERVER = "ntp.shoa.cl"

def main():
    user = input("Username: ")
    password = getpass.getpass("Password: ")

    with open(HOSTS_FILE, "r", encoding="utf-8") as f:

        for line in f:
            ip = line.strip()
            if not ip or ip.startswith("#"):
                continue

            try:            
                print(f"Cambiando horario switch/router {ip}")
                tn = telnetlib.Telnet()
                tn.open(ip, 23, timeout=10)

                tn.expect([b"Username", b"username"],12)
                tn.write(user.encode("ascii") + b"\r\n")

                if password:
                    tn.expect([b"Password", b"password"],12)
                    tn.write(password.encode("ascii") + b"\r\n")

                    tn.write(b"config t\n")
                    tn.write(f"clock timezone {TZ_OFFSET}\n".encode("ascii"))
                    tn.write(f"ntp server {NTP_SERVER}\n".encode("ascii"))
                    tn.write(b"exit\n")
                    tn.write(b"write\n")
                    tn.write(b"exit\n")

                    readoutput = (tn.read_all().decode("ascii"))
                    print(str(readoutput))
                    tn.close()
            except (socket.timeout, ConnectionRefusedError) as e:
                print(f"[ERROR] {ip} Timeout {e}")
            except Exception as e:
                print(f"[ERROR] {ip} {e}")

if __name__ == "__main__":
    main()
