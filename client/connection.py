import socket
import threading

server_ip = "57.158.27.23"
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

def receive_udp_message(callback):
    """Receive UDP messages from the server."""
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("", udp_port))
    print(f"UDP listener started on port {udp_port}")
    
    while True:
        try:
            data, addr = udp_sock.recvfrom(1024)
            callback(data.decode())
        except Exception as e:
            print(f"Error receiving UDP message: {e}")

if __name__ == "__main__":
    client_socket = get_connection(server_ip, server_port)

    threading.Thread(target=send_message, args=(client_socket, "Hello, Server!"), daemon=True).start()
