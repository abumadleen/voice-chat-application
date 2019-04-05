import socket
from _thread import *

def clientSendThread(clientSocket):
    while 1:
        _input = input()    
        clientSocket.send(_input.encode())
serverName = '127.0.0.1'
serverPort = 8585
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
start_new_thread(clientSendThread,(clientSocket,))
while 1:
    response = clientSocket.recv(1024)
    print(response)
    # _input = input()
# clientSocket.close()
