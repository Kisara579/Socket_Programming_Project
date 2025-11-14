import customtkinter
import tkinter as tk
import threading

from connection import get_connection, send_message, receive_message, server_ip, server_port

client_socket = get_connection(server_ip, server_port)

def send_button_click():
    """Handles sending a message and displaying it on the UI."""
    message = message_entry.get()
    if message:
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

        def _show_menu(event):
            menu = tk.Menu(None, tearoff=0)
            menu.add_command(label="Delete", command=bubble.destroy)
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        bubble.bind("<Button-3>", _show_menu)

        try:
            app.after(10, messages_container._parent_canvas.yview_moveto, 1.0)
        except Exception:
            pass

    try:
        app.after(0, _create_bubble)
    except Exception:
        try:
            _create_bubble()
        except Exception as e:
            print(f"Error creating bubble: {e}\nMessage: {message}")

threading.Thread(
    target=receive_message, 
    args=(client_socket, add_message_to_ui), 
    daemon=True
).start()


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
header_label.pack(padx=12, pady=12, anchor="w")

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

send_button = customtkinter.CTkButton(
    input_frame, 
    text="Send", 
    command=send_button_click,
    width=70,
    height=36,
    corner_radius=18,
    fg_color="#075E54",
    hover_color="#054D44"
)
send_button.grid(row=0, column=1, padx=(6, 10), pady=10)


app.mainloop()

print("Closing connection...")
client_socket.close()