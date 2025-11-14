import socket
import threading

server_ip = "20.205.16.74"
server_port = 8888


def get_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def send_message(conn):
    while True:
        message = input()
        conn.send(message.encode())

def receive_message(conn):
    while True:
        data = conn.recv(1024)
        print(data.decode())

client_socket = get_connection(server_ip, server_port)

threading.Thread(target=send_message, args=(client_socket,)).start()
threading.Thread(target=receive_message, args=(client_socket,)).start()
