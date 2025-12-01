# Socket Programming Chat Application

A real-time chat application built with Python, featuring both TCP and UDP communication protocols with a modern graphical user interface.

## 📋 Project Overview

This is a project related to CSCI 21023 - Data Communication and Networks. The application demonstrates socket programming concepts with a client-server architecture that supports both reliable (TCP) and unreliable (UDP) communication protocols.

## ✨ Features

- **Dual Protocol Support**: Switch between TCP and UDP messaging seamlessly
- **Real-time Messaging**: Instant message delivery across connected clients
- **Modern GUI**: Clean, WhatsApp-inspired interface built with CustomTkinter
- **Multi-client Support**: Server handles multiple simultaneous connections
- **Thread-safe Operations**: Proper synchronization for concurrent message handling
- **Message Deduplication**: UDP messages are filtered to prevent echoes
- **Auto-reconnection**: Visual status indicators with reconnection capability

## 🏗️ Architecture

### Server (`server/main.py`)

- **TCP Server**: Listens on port 8888 for persistent client connections
- **UDP Server**: Listens on port 9999 for connectionless messaging
- **Broadcasting**: Messages are relayed to all connected clients
- **Thread Management**: Each TCP client is handled in a separate thread
- **Client Management**: Automatic cleanup of disconnected clients

### Client (`client/`)

#### Connection Module (`connection.py`)

- **TCP Connection**: Reliable stream-based communication
- **UDP Socket**: Shared, thread-safe UDP socket with automatic registration
- **Message Deduplication**: Prevents receiving own UDP messages
- **Background Listeners**: Separate threads for TCP and UDP message reception

#### Main Application (`main.py`)

- **CustomTkinter GUI**: Modern, responsive chat interface
- **Protocol Toggle**: Switch between TCP and UDP modes
- **Message Bubbles**: Visual distinction between sent and received messages
- **Error Handling**: User-friendly error dialogs and status indicators
- **Async Connection**: Non-blocking server connection with status updates

## 🚀 Getting Started

### Prerequisites

```bash
pip install customtkinter
```

### Server Setup

1. Navigate to the server directory:

```bash
cd server
```

2. Run the server:

```bash
python main.py
```

The server will start listening on:

- TCP: `0.0.0.0:8888`
- UDP: `0.0.0.0:9999`

### Client Setup

1. Update server IP in `client/connection.py`:

```python
server_ip = "YOUR_SERVER_IP"
server_port = 8888
udp_port = 9999
```

2. Navigate to the client directory:

```bash
cd client
```

3. Run the client:

```bash
python main.py
```

## 🎮 Usage

### Sending Messages

1. **TCP Mode (Default)**:

   - Type your message in the input field
   - Press Enter or click "Send"
   - Message is reliably delivered to all connected clients

2. **UDP Mode**:
   - Click the "TCP" button to switch to "UDP"
   - Type and send messages
   - Messages are prefixed with `[UDP]` tag
   - Delivery is not guaranteed but faster

### Connection Status

- **Yellow "Connecting..."**: Initial connection attempt
- **Green "Connected"**: Successfully connected to server
- **Red "Disconnected, Retry?"**: Connection failed (click to retry)

### Message Display

- **Green bubbles (right)**: Your sent messages
- **White bubbles (left)**: Received messages from others
- **Red bubbles (center)**: Error messages

## 🔧 Technical Details

### TCP Communication Flow

1. Client establishes connection with server
2. Server adds client to active connections list
3. Messages are sent to server via `send_message()`
4. Server broadcasts to all other connected clients
5. Clients receive via `receive_message()` callback

### UDP Communication Flow

1. Client creates/reuses shared UDP socket
2. Registration message sent to server on first use
3. Server tracks UDP client addresses
4. Messages include unique timestamp ID
5. Clients filter out their own messages using ID matching
6. No delivery guarantee or ordering

### Key Components

#### Server-Side

- `handle_client()`: Manages individual TCP connections
- `udp_echo()`: Broadcasts UDP messages to registered clients
- `tcp_server()`: Accepts new TCP connections
- `udp_server()`: Listens for UDP datagrams

#### Client-Side

- `_get_udp_socket()`: Singleton pattern for UDP socket
- `_SocketProxy`: Delayed socket initialization for UI responsiveness
- `add_message_to_ui()`: Thread-safe UI updates
- `send_button_click()`: Protocol-aware message sending

## 🛡️ Error Handling

- **Connection Failures**: Graceful error dialogs with retry option
- **Broken Pipes**: Automatic client cleanup on disconnection
- **Thread Safety**: Locks prevent race conditions in UDP socket access
- **Message Send Failures**: Error bubbles displayed in chat

## 📁 Project Structure

```
Socket_Programming_Project/
├── README.md
├── client/
│   ├── connection.py      # Network communication logic
│   ├── main.py           # GUI application
│   └── __pycache__/
└── server/
    └── main.py           # Server implementation
```

## 🔒 Security Considerations

⚠️ **Note**: This is an educational project and lacks production-ready security features:

- No encryption (messages sent in plaintext)
- No authentication or authorization
- No input validation or sanitization
- Public IP exposure in code

For production use, implement:

- TLS/SSL encryption
- User authentication
- Input validation
- Rate limiting
- Secure configuration management

## 🐛 Known Issues

- UDP message deduplication clears all IDs after 100 messages (memory optimization)
- Server IP is hardcoded in `connection.py`
- No persistent message history
- No file transfer support

## 🤝 Contributing

This is an academic project. Feel free to fork and extend for learning purposes.

## 📝 License

Educational project for CSCI 21023 course.

## 👥 Authors

Socket Programming Project Team
chamesh2019
kisara579
SanjanaKaushalya

## 🙏 Acknowledgments

- CSCI 21023 - Data Communication and Networks course
- CustomTkinter library for modern UI components
- Python socket programming documentation
