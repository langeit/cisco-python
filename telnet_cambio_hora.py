#!/usr/bin/python
# @author [Mauricio Lange]
# @email [mlangea@gestion.uta.cl]
# @create date 2025-04-01 15:00
# @desc [Automation - Configura Servidor NTP y Zona Horaria a Horario Verano/Invierno en Chile]
# UTC -3 = Verano
# UTC -4 = Invierno
import getpass
import sys
import telnetlib

HOST = ""
user = input("Username: ")
password = getpass.getpass()

file = open("hosts")

for IP in file:
    IP = IP.strip()
    print('Cambiando horario switch/router ' + IP)
    HOST = IP
    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
    
        tn.write(b"config t\n")
        tn.write(b"clock timezone UTC -3 0\n")
        tn.write(b"ntp server ntp.shoa.cl\n")
        tn.write(b"exit\n")
        tn.write(b"exit\n")
    
        readoutput = (tn.read_all().decode("ascii"))
        print(str(readoutput))
        tn.close()
