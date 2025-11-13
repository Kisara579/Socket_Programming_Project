import socket

server_ip = "20.205.16.74"
server_port = 8888

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    client_socket.connect((server_ip,server_port))
    print("Connected to server")
except Exception as e:
    print("Connection Failed:",e)
    exit()

    