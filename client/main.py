import socket
import threading

server_ip = "20.205.16.74"
server_port = 8888

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

def send_message():
    while True:
        message = input()
        client_socket.send(message.encode())

def receive_message():
    while True:
        data = client_socket.recv(1024)
        print(data.decode())


threading.Thread(target=send_message).start()
threading.Thread(target=receive_message).start()
