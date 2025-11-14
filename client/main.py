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

    
def send_message():
    while True:
        message = input()
        if message.lower() == "exit":
            client_socket.close()
            print("You left the chat")
            break
        client_socket.send(message.encode())

def receive_message():
    while True:
        data = client_socket.recv(1024)
        print(data.decode())


