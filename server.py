import socket
from _thread import *


clients = []
conn_sockets = {}

def clientThread(conn,addr):
    """ for a client thread run this function"""
    print(str(addr)+" connected to server.")
    global kir
    global text
    kir = ""
    text = ""
    while 1:
        # print("Text is:",text,kir)
        command = conn.recv(1024)
        output = "None".encode()
        print("Recieve:",command)
        decode_command = str(command.decode())
        if decode_command =="get":
            cli = [str(i) for i in conn_sockets.items()]
            output = '&'.join(cli)
            conn.send(output.encode())
            print(output)
        elif decode_command =="y":
            
            selectedConnection = conn_sockets[kir]
            selectedConnection.send(text.encode())
        else:
            commands = decode_command.split()
            # if decode_command !="y":
            dest_ip = commands[1]
            dest_port = commands[2]
            text = commands[3:]
            conn.send("Pending...".encode())
            dest = "('{0}', {1})".format(dest_ip,dest_port)
            kir = dest
            selectedConnection = conn_sockets[dest]
            selectedConnection.send("Client {0} wants to connect to you. do you accept or reject?".format(addr).encode()) 
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
    serverSocket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    serverSocket.bind(('127.0.0.1',server_port))
    serverSocket.listen(5)
    print("Server is ready to receiving data...")
    while 1:
        connectionSocket , addr = serverSocket.accept()
        clients.append(addr)
        conn_sockets[str(addr)] = connectionSocket
        start_new_thread(clientThread,(connectionSocket,addr,))
        # print(clients)
except IndexError as e:
    exit()
    