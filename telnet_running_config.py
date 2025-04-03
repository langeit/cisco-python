#!/usr/bin/python
import telnetlib
import getpass

HOST = "hosts"
ciscouser = input("Username : ")
ciscopass = getpass.getpass()
#print('enable password')
#enable = getpass.getpass()

file = open("hosts")

for IP in file:
    IP = IP.strip()
    print('Obtiene configuracion de switch/router ' + IP)
    HOST = IP
    tn = telnetlib.Telnet(HOST)
    tn.read_until(b"Username: ")
    tn.write(ciscouser.encode('ascii') + b"\n")
    if ciscopass:
        tn.read_until(b"Password:")
        tn.write(ciscopass.encode('ascii') + b"\n")

    #tn.write(b"en\n")
    #tn.write(ciscopass.encode('ascii') + b"\n")
    tn.write(b"terminal leng 0\n")
    tn.write(b"sh run\n")
    tn.write(b"exit\n")

    readoutput = (tn.read_all().decode("ascii"))
    saveoutput = open("backup " + HOST + ".txt", 'w')
    saveoutput.write(str(readoutput))
    saveoutput.write("\n")
    tn.close()