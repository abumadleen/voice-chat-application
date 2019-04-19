from socket import *
from _thread import *



def serverReciveThenSend(port_number, tcp_client_socket, target):
    server_port = port_number
    server_ip = '127.0.0.1'
    udp_serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_serverSocket.bind((server_ip, server_port))
    print("Server is reade for receiving data...")

    data, clientAddress = udp_serverSocket.recvfrom(1024)
    f = open(r"f1.mp3", 'wb+')
    while data:
        f.write(data)
        data, clientAddress = udp_serverSocket.recvfrom(1024)
        if data==bytes("kir",encoding='utf8'):
            print("File Downloaded.")
            break
    f.close()
    send_data(target, tcp_client_socket, udp_serverSocket)


def send_data(clientSocket, tcp_client_socket, server_socket):
    data = {"status": "ack"}
    ser_data = dumps(data).encode()
    tcp_client_socket.send(ser_data)
    buf = 1024
    f1 = open("f1.mp3", 'rb')
    print("Klient   ",clientSocket)
    data = f1.read(buf)
    while data:
        if server_socket.sendto(data, clientSocket):
            print("sending > > > > >000000000")
            data = f1.read(buf)





##############################################

import socket
from json import *
from _thread import *

clients = []
conn_sockets = {}
udp_sockets = {}


def clientThread(conn, addr):
    """ for a client thread run this function"""
    print(str(addr) + " connected to server.")
    global kir
    global kirB
    global text
    kir = ""
    kirB = ""
    text = ""
    while 1:
        # print("Text is:",text,kir)
        command = conn.recv(1024)
        output = "None".encode()
        print("Recieve:", command)
        decode_command = str(command.decode())
        if decode_command == "get":
            cli = [str(i) for i in conn_sockets.items()]
            output = '&'.join(cli)
            dt = dumps({"status":output}).encode()
            conn.send(dt)
            print(output)
        elif decode_command == "y":
            # selectedConnection = conn_sockets[kir]
            data = {"status": "accepted", "file_name": text}
            ser_data = dumps(data)
            clA = conn_sockets[kirB]
            clA.send(ser_data.encode())  # server request to client A to send his file...
            print(udp_sockets)
            serverReciveThenSend(12001, clA, udp_sockets[kirB])  # server waiting to receive file from client A then send it to client B
            print("file downloaded")

        elif decode_command == "n":  # client c2 reject connection from client c1
            data = {"status": "Client c2 rejected your connection."}
            ser_data = dumps(data)
            clA = conn_sockets[kirB]
            clA.send(ser_data.encode())

        else:  # send from client1 to client2
            commands = decode_command.split()
            dest_ip = commands[1]
            dest_port = commands[2]
            text = commands[3:]
            conn.send(dumps({"status":"Pending"}).encode())
            dest = "('{0}', {1})".format(dest_ip, dest_port)
            kir = dest
            kirB = str(addr)
            selectedConnection = conn_sockets[dest]
            data = {"status": "Client {0} wants to connect to you. do you accept or reject?".format(addr)}
            ser_data = dumps(data)
            selectedConnection.send(ser_data.encode())
            # status = selectedConnection.recv(1024).decode()
            # print(commands)
            # if status=="y":
            #     selectedConnection.send(text.encode())
        # connectionSocket.close()
        # clients.remove(addr)
        # clients.remove(addr)
        # connectionSocket.close()
        # print(clients)


try:
    server_port = 8585
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', server_port))
    serverSocket.listen(5)
    server_ip = '127.0.0.1'
    udp_serverSocket = socket.socket(AF_INET, SOCK_DGRAM)
    udp_serverSocket.bind((server_ip, 12000))

    print("Server is ready to receiving data...")
    while 1:
        connectionSocket, addr = serverSocket.accept()
        data, clientAddress = udp_serverSocket.recvfrom(1024)
        print("udp address is",clientAddress)
        # udp_serverSocket.close()
        clients.append(addr)
        udp_sockets[str(addr)] = clientAddress
        conn_sockets[str(addr)] = connectionSocket
        start_new_thread(clientThread, (connectionSocket, addr,))
        # print(clients)
except KeyboardInterrupt as e:
    serverSocket.close()
    udp_serverSocket.close()
    connectionSocket.close()
    print(repr(e))
    exit()
