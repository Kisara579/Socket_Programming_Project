import socket
import threading

HOST = "0.0.0.0"
PORT = 8888
UDP_PORT = 9999

clients = []
udp_clients = []

def handle_client(conn, addr):
    """Handle a single client connection: echo received data back until closed."""
    with conn:
        print(f"Connected by {addr}")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                for c, a in clients[:]:
                    if c == conn:
                        continue
                    try:
                        c.sendall(data)
                    except (BrokenPipeError, ConnectionResetError, OSError) as e:
                        print(f"Error sending to {a}: {e}. Removing client.")
                        try:
                            c.close()
                        except Exception:
                            pass
                        try:
                            clients.remove((c, a))
                        except ValueError:
                            pass
        except ConnectionResetError:
            print(f"Connection reset by {addr}")
        finally:
            print(f"Connection with {addr} closed")

def udp_echo(data, addr, udp_sock):
    print(f"Received UDP data from {addr}")

    if addr not in udp_clients:
        udp_clients.append(addr)
    for c_addr in udp_clients[:]:
        try:
            udp_sock.sendto(data, c_addr)
        except OSError as e:
            print(f"Error sending to {c_addr}: {e}. Removing UDP client.")
            try:
                udp_clients.remove(c_addr)
            except ValueError:
                pass

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            clients.append((conn, addr))
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()


def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_sock.bind((HOST, UDP_PORT))
        print(f"UDP server listening on {HOST}:{UDP_PORT}")
        while True:
            data, addr = udp_sock.recvfrom(1024)
            udp_echo(data, addr, udp_sock)

def main():
    tcp_thread = threading.Thread(target=tcp_server, daemon=True)
    tcp_thread.start()
    udp_thread = threading.Thread(target=udp_server, daemon=True)
    udp_thread.start()
    tcp_thread.join()
    udp_thread.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Server shutting down")