import socket
import threading

HOST = "0.0.0.0"
PORT = 8888
clients = []

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


def main():
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Server shutting down")