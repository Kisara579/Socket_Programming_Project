import socket
import threading

server_ip = "20.205.16.74"
server_port = 8888


def get_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print(f"Connected to server at {host}:{port}")
    return s

def send_message(conn, message):
    conn.send(message.encode())

def receive_message(conn, callback):
    while True:
        data = conn.recv(1024)
        callback(data.decode())

if __name__ == "__main__":
    client_socket = get_connection(server_ip, server_port)

    threading.Thread(target=send_message, args=(client_socket, "Hello, Server!"), daemon=True).start()
