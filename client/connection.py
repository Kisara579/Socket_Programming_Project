import socket
import threading

server_ip = "20.205.16.74"
# server_ip = "127.0.0.1"
server_port = 8888
udp_port = 9999

def get_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print(f"Connected to server at {host}:{port}")
    return s

def send_message(conn, message):
    conn.send(message.encode())

def send_udp_message(message, server_address):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(("", 0))
    udp_sock.sendto(message.encode(), (server_address, udp_port))
    udp_sock.close()

def receive_message(conn, callback):
    while True:
        data = conn.recv(1024)
        callback(data.decode())

if __name__ == "__main__":
    client_socket = get_connection(server_ip, server_port)

    threading.Thread(target=send_message, args=(client_socket, "Hello, Server!"), daemon=True).start()
