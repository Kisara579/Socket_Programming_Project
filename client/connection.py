import socket
import threading

server_ip = "127.0.0.1"  # localhost for testing
server_port = 8888
udp_port = 9999

# Shared UDP socket
_udp_socket = None
_udp_lock = threading.Lock()

def _get_udp_socket():
    """Get or create the shared UDP socket."""
    global _udp_socket
    with _udp_lock:
        if _udp_socket is None:
            _udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            _udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            _udp_socket.bind(("", udp_port))
            print(f"UDP socket bound to port {udp_port}")
        return _udp_socket

def get_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print(f"Connected to server at {host}:{port}")
    return s

def send_message(conn, message):
    conn.send(message.encode())

def send_udp_message(message, server_address):
    udp_sock = _get_udp_socket()
    udp_sock.sendto(message.encode(), (server_address, udp_port))

def receive_message(conn, callback):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            callback(data.decode())
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def receive_udp_message(callback):
    """Receive UDP messages from the server."""
    udp_sock = _get_udp_socket()
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
