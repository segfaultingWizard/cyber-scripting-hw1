import socket
import hashlib

port = 8080
chunksize = 1024
hashAlgorithm = 'sha256'

def sendFile(mySocket, path):
    # https://www.geeksforgeeks.org/python/how-to-get-file-size-in-python/
    #socket.send(os.path.getsize(path)

    fileHash = hashlib.new(hashAlgorithm)
    with open(path, 'rb') as file:
        # walrus operator so we loop for the whole file
        while packet := file.read(chunksize):
            # https://www.geeksforgeeks.org/python/python-program-to-find-hash-of-file/
            fileHash.update(packet)
            mySocket.send(packet)
    mySocket.send('DONE'.encode())
    hexdigest = fileHash.hexdigest()
    returnPacket = ''
    while returnPacket != 'READY':
        returnPacket = mySocket.recv(chunksize).decode()
    mySocket.send(hexdigest.encode())
