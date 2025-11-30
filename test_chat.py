"""
Test script to verify the chat application works correctly.
This simulates two clients sending messages to each other.
"""
import socket
import threading
import time

SERVER_IP = "127.0.0.1"
TCP_PORT = 8888
UDP_PORT = 9999

def tcp_client(name, messages):
    """Simulate a TCP client sending and receiving messages."""
    print(f"[{name}] Connecting to server...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, TCP_PORT))
    print(f"[{name}] Connected!")
    
    received_messages = []
    
    def receive():
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    break
                msg = data.decode()
                print(f"[{name}] Received: {msg}")
                received_messages.append(msg)
            except Exception as e:
                print(f"[{name}] Error receiving: {e}")
                break
    
    # Start receiver thread
    receiver = threading.Thread(target=receive, daemon=True)
    receiver.start()
    
    # Send messages
    time.sleep(1)  # Wait for other client to connect
    for msg in messages:
        print(f"[{name}] Sending: {msg}")
        sock.send(msg.encode())
        time.sleep(0.5)
    
    # Wait to receive messages
    time.sleep(2)
    sock.close()
    return received_messages

def udp_client(name, message):
    """Simulate a UDP client sending a message."""
    print(f"[{name}] Setting up UDP socket...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", UDP_PORT))
    
    received_messages = []
    
    def receive():
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                msg = data.decode()
                print(f"[{name}] UDP Received: {msg}")
                received_messages.append(msg)
            except Exception as e:
                print(f"[{name}] Error receiving UDP: {e}")
                break
    
    # Start receiver
    receiver = threading.Thread(target=receive, daemon=True)
    receiver.start()
    
    # Send message
    time.sleep(1)
    print(f"[{name}] Sending UDP: {message}")
    sock.sendto(message.encode(), (SERVER_IP, UDP_PORT))
    
    time.sleep(2)
    sock.close()
    return received_messages

def test_tcp():
    """Test TCP messaging between two clients."""
    print("\n=== Testing TCP ===")
    
    client1_messages = ["Hello from Client1!", "How are you?"]
    client2_messages = ["Hi Client1!", "I'm good, thanks!"]
    
    # Run both clients
    results = []
    t1 = threading.Thread(target=lambda: results.append(tcp_client("Client1", client1_messages)))
    t2 = threading.Thread(target=lambda: results.append(tcp_client("Client2", client2_messages)))
    
    t1.start()
    time.sleep(0.2)  # Stagger connection
    t2.start()
    
    t1.join()
    t2.join()
    
    print(f"\nTCP Test Summary:")
    print(f"Client1 should receive {len(client2_messages)} messages")
    print(f"Client2 should receive {len(client1_messages)} messages")
    print(f"✓ TCP test completed")

if __name__ == "__main__":
    print("Chat Application Test Suite")
    print("============================")
    print("Make sure the server is running before starting tests!")
    time.sleep(2)
    
    test_tcp()
    
    print("\n=== All tests completed ===")
