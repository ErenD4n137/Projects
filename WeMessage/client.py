import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

client = socket.socket()
client.connect(("localhost", 12345))

username = input("Enter username: ")
client.send(username.encode())

# ---------------- GUI STARTS ONLY AFTER ---------------- #

window = tk.Tk()
window.title(f"WeMessage - {username}")

bg_image = Image.open("Movie App\\images\\3f54839dc63eeef1328f7f7652fc34ff.jpg")
bg_image = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# CHAT DISPLAY (scrollable)
chat_box = scrolledtext.ScrolledText(window, width=50, height=20, bg="#f0f0f0", fg="#000000", font=("Arial", 12))
chat_box.pack()
chat_box.config(state='disabled')  # read-only


# INPUT FIELD
entry = tk.Entry(window, width=40)
entry.pack()

# SEND FUNCTION
def send_message():
    message = entry.get()
    if message:
        client.send(message.encode())
        entry.delete(0, tk.END)

        chat_box.config(state='normal')
        chat_box.insert(tk.END, f"You: {message}\n")
        chat_box.config(state='disabled')
        chat_box.yview(tk.END)

# ENTER KEY SUPPORT
window.bind('<Return>', lambda event: send_message())

btn = tk.Button(window, text="Send", command=send_message)
btn.pack()

# RECEIVE THREAD
def receive():
    while True:
        try:
            message = client.recv(1024).decode()

            chat_box.config(state='normal')
            chat_box.insert(tk.END, message + "\n")
            chat_box.config(state='disabled')
            chat_box.yview(tk.END)

        except:
            break

threading.Thread(target=receive, daemon=True).start()

window.mainloop()