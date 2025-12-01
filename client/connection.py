import socket
import threading
import time

server_ip = "57.158.27.23"
server_port = 8888
udp_port = 9999

# Shared UDP socket
_udp_socket = None
_udp_lock = threading.Lock()
_sent_messages = set()  # Use set for O(1) lookup

def _get_udp_socket():
    """Get or create the shared UDP socket."""
    global _udp_socket
    with _udp_lock:
        if _udp_socket is None:
            _udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            _udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            _udp_socket.bind(("", 0))
            # Register with server immediately so it can send messages to us
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
    id = str(time.time())  # Convert to string immediately
    _sent_messages.add(id)  # Use set.add instead of list.append
    udp_sock.sendto((id + " " + message).encode(), (server_address, udp_port))

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
    print(f"UDP listener started on port {udp_sock.getsockname()[1]}")
    
    while True:
        try:
            data, addr = udp_sock.recvfrom(1024)
            id, message = data.decode().split(" ", 1)
            if id in _sent_messages:
                # Clean up old messages to prevent memory leak (keep last 100)
                if len(_sent_messages) > 100:
                    _sent_messages.clear()
                continue
            callback(message)
        except Exception as e:
            print(f"Error receiving UDP message: {e}")

if __name__ == "__main__":
    client_socket = get_connection(server_ip, server_port)

    threading.Thread(target=send_message, args=(client_socket, "Hello, Server!"), daemon=True).start()
