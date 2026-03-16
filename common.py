import socket
import hashlib
import os
import sys

port = 8080
chunksize = 1024
hashAlgorithm = 'sha256'

# Source - https://stackoverflow.com/a/10270732
# Posted by frnknstn, modified by community and here. See post 'Timeline' for change history
# Retrieved 2026-03-12, License - CC BY-SA 4.0
# https://stackoverflow.com/questions/1319615/how-do-i-declare-custom-exceptions-in-modern-python/10270732#10270732
class HashMatchError(Exception):
    def __init__(self, remoteFileHash, localFileHash):
        message = """[-] Warning! File hashes do not match.
Remote file hash: {hash1}
Local file hash: {hash2}""".format(hash1=remoteFileHash, hash2=localFileHash)
        super().__init__(message)

# Source - https://stackoverflow.com/a/45669280
# Posted by Alexander C, modified by community and here. See post 'Timeline' for change history
# Retrieved 2026-03-12, License - CC BY-SA 4.0
# https://stackoverflow.com/questions/8391411/how-to-block-calls-to-print/45669280#45669280
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

# https://sqlpey.com/python/top-8-methods-to-hash-files-in-python/
def getFileHash(filePath):
    fileHash = hashlib.new(hashAlgorithm)
    with open(filePath, 'rb') as file:
        while chunk := file.read(fileHash.block_size):
            fileHash.update(chunk)
    return fileHash.hexdigest()

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

def receiveFile(mySocket, destinationFile):
    try:
        os.mkdir(os.path.dirname(destinationFile))
        print('Created destination folder')
    except FileExistsError:
        print('Destination folder exists')

    print('[+] Destination File=', destinationFile)

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
                    return 0
                else:
                    raise HashMatchError(remoteFileHash, localFileHash)
            elif 'File not found'.encode() in packet:
                print ('[-] File not found')
                return 2
            elif 'ERROR'.encode() in packet:
                error = packet.decode().split('ERROR')[1:]
                print(error)
                return 3
            file.write(packet)
