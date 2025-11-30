import customtkinter
import tkinter as tk
import threading
from tkinter import  messagebox

from connection import get_connection, send_message, receive_message, server_ip, server_port, send_udp_message, receive_udp_message

connected = False
isUDP = False

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.title("Chat")
app.geometry("400x650")

app.grid_rowconfigure(1, weight=1) 
app.grid_rowconfigure(0, weight=0) 
app.grid_rowconfigure(2, weight=0)
app.grid_columnconfigure(0, weight=1)

header_frame = customtkinter.CTkFrame(app, fg_color="#075E54", corner_radius=0)
header_frame.grid(row=0, column=0, sticky="ew")

header_label = customtkinter.CTkLabel(
    header_frame, 
    text="Chat", 
    font=("Helvetica", 20, "bold"), 
    text_color="white"
)

status_label = customtkinter.CTkLabel(
    header_frame,
    text="Connecting...",
    font=("Helvetica", 16),
    text_color="yellow",
)
status_label.bind("<Button-1>", lambda event: _connect_background())

header_frame.grid_columnconfigure(0, weight=1)
header_label.grid(row=0, column=0, sticky="w", padx=12, pady=12)
status_label.grid(row=0, column=1, sticky="e", padx=12, pady=(0, 8))

messages_container = customtkinter.CTkScrollableFrame(app, fg_color="#EBEBEB", corner_radius=0)
messages_container.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

input_frame = customtkinter.CTkFrame(app, fg_color="#F0F0F0", corner_radius=0)
input_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
input_frame.grid_columnconfigure(0, weight=1)

message_entry = customtkinter.CTkEntry(
    input_frame, 
    placeholder_text="Type a message...",
    fg_color="#FFFFFF",
    border_width=0,
    corner_radius=18,
    text_color="#000000"
)
message_entry.grid(row=0, column=0, sticky="ew", padx=(10, 6), pady=10)

message_entry.bind("<Return>", lambda event: send_button_click())

typeButton = customtkinter.CTkButton(
    input_frame, 
    text="TCP" if not isUDP else "UDP", 
    width=70,
    height=36,
    corner_radius=18,
    fg_color="#075E54",
    hover_color="#054D44"
)

typeButton.grid(row=0, column=2, padx=(0, 10), pady=10)

def toggle_protocol():
    global isUDP
    isUDP = not isUDP
    typeButton.configure(text="TCP" if not isUDP else "UDP")

typeButton.configure(command=toggle_protocol)

send_button = customtkinter.CTkButton(
    input_frame, 
    text="Send",
    width=70,
    height=36,
    corner_radius=18,
    fg_color="#075E54",
    hover_color="#054D44"
)

send_button.grid(row=0, column=1, padx=(6, 10), pady=10)

send_button.bind("<Button-1>", lambda event: send_button_click())


def show_error_dialog(message: str) -> None:
    """Displays an error dialog with the given message using a hidden root so no parent window is shown."""
    try:
        messagebox.showerror("Connection Error", message, parent=app)
    except Exception:
        pass


class _SocketProxy:
    def __init__(self):
        self._ready = threading.Event()
        self._sock = None
        self._error = None

    def set_socket(self, sock):
        self._sock = sock
        self._ready.set()

    def set_error(self, exc):
        self._error = exc
        self._ready.set()

    def __getattr__(self, name):
        def _call(*args, **kwargs):
            self._ready.wait()
            if self._error:
                raise self._error
            return getattr(self._sock, name)(*args, **kwargs)
        return _call

client_socket = _SocketProxy()

def _connect_background():
    global connected
    try:
        sock = get_connection(server_ip, server_port)
        client_socket.set_socket(sock)
        connected = True
        app.after(0, lambda: status_label.configure(text="Connected"))
    except Exception as e:
        print(f"Could not connect to server at {server_ip}:{server_port}: {e}")
        connected = False
        app.after(0, lambda: status_label.configure(text="Disconnected, Retry?"))
        client_socket.set_error(e)
        try:
            show_error_dialog(f"Could not connect to server at {server_ip}:{server_port}.\nPlease try again later.")
        except Exception:
            pass

threading.Thread(target=_connect_background, daemon=True).start()



def send_button_click():
    """Handles sending a message and displaying it on the UI."""
    if not connected:
        show_error_dialog("Not connected to server. Please try reconnecting.")
        return

    message = message_entry.get()
    if message:
        if isUDP:
            message = f"[UDP] {message}"
            try:
                send_udp_message(message, server_ip)
                add_message_to_ui(message, origin='sent')
                message_entry.delete(0, tk.END)
                return
            except Exception as e:
                print(f"Error sending UDP message: {e}")
                add_message_to_ui(f"Error: Could not send message '{message}'", origin='error')
                return
        try:
            send_message(client_socket, message)
            add_message_to_ui(message, origin='sent')
            message_entry.delete(0, tk.END)
        except Exception as e:
            print(f"Error sending message: {e}")
            add_message_to_ui(f"Error: Could not send message '{message}'", origin='error')


def add_message_to_ui(message: str, origin: str = 'received') -> None:
    """
    Adds a message bubble to the chat UI.
    'origin' can be 'received', 'sent', or 'error'.
    """
    
    if 'messages_container' not in globals():
        print(message)
        return

    def _create_bubble():
        if origin == 'sent':
            # Sent messages: light green, aligned right
            bubble_bg = "#DCF8C6"
            text_color = "#000000"
            anchor = "e"
            padx = (60, 8) # More padding on the left
            justify = "right"
        elif origin == 'received':
            # Received messages: white, aligned left
            bubble_bg = "#FFFFFF"
            text_color = "#000000"
            anchor = "w"
            padx = (8, 60) # More padding on the right
            justify = "left"
        else: # 'error' or other
            # Error messages: light red, centered
            bubble_bg = "#FFD2D2"
            text_color = "#D8000C"
            anchor = "center"
            padx = (8, 8)
            justify = "center"

        bubble = customtkinter.CTkFrame(messages_container, fg_color=bubble_bg, corner_radius=10)
        
        label = customtkinter.CTkLabel(
            bubble, 
            text=message, 
            text_color=text_color, 
            wraplength=280,
            justify=justify
        )
        label.pack(padx=10, pady=6)

        bubble.pack(anchor=anchor, pady=6, padx=padx, fill='x', expand=False)

threading.Thread(
    target=receive_message, 
    args=(client_socket, add_message_to_ui), 
    daemon=True
).start()

# Start UDP receiver thread
threading.Thread(
    target=receive_udp_message,
    args=(add_message_to_ui,),
    daemon=True
).start()

app.mainloop()

print("Closing connection...")
client_socket.close()