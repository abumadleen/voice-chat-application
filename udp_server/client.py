from _thread import start_new_thread
from socket import *
# import pyaudio
import time

frames = []


def ReceiveFromServer(udp_clientSocket):
    data, clientAddress = udp_clientSocket.recvfrom(1024)
    f = open(r"audio/kir_{0}.mp3".format(time.time()), 'wb+')
    while data:
        f.write(data)
        frames.append(data)
        data, clientAddress = udp_clientSocket.recvfrom(1024)
    f.close()


def play(stream, CHUNK):
    BUFFER = 10
    while True:
        if len(frames) == BUFFER:
            while True:
                stream.write(frames.pop(0), CHUNK)


def sendFromClient(udp_port_number, file_name):
    serverName = '127.0.0.1'
    serverPort = udp_port_number
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    buf = 1024
    f1 = open("f1.mp3", 'rb')
    data = f1.read(buf)
    while data:
        if clientSocket.sendto(data, (serverName, serverPort)):
            print("sending > > > > >")
            data = f1.read(buf)
    else:
        print("file sent")
        clientSocket.sendto(bytes("kir", encoding='utf8'), (serverName, serverPort))
    # clientSocket.sendto(message.encode(),(serverName, serverPort))
    # modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    # print(modifiedMessage.decode())
    # clientSocket.close()


######################################################################

from json import *
from _thread import *


def clientSendThread(clientSocket):
    while 1:
        _input = input()
        clientSocket.send(_input.encode())


serverName = '127.0.0.1'
serverPort = 8585
udp_server_port = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
serverName = '127.0.0.1'
udp_clientSocket = socket(AF_INET, SOCK_DGRAM)
udp_clientSocket.sendto("hello".encode(), (serverName, udp_server_port))
start_new_thread(clientSendThread, (clientSocket,))

while 1:
    response = clientSocket.recv(1024)
    deserialize_response = loads(response.decode())
    status = deserialize_response["status"]
    print(status)
    if status == "accepted":
        sendFromClient(12001, deserialize_response["file_name"])  # upload from c1 to server
    elif status == "ack":
        print("file downloaded")
        # FORMAT = pyaudio.paInt16
        data, clientAddress = udp_clientSocket.recvfrom(1024)
        f = open(r"audio/kirCos.mp3", 'wb+')
        while data:
            f.write(data)
            data, clientAddress = udp_clientSocket.recvfrom(1024)
        f.close()

# _input = input()
# clientSocket.close()
