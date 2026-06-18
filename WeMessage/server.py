import socket
import threading
import sqlite3
from datetime import datetime

# ---------------- DATABASE ---------------- #
db = sqlite3.connect("chat.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    message TEXT,
    timestamp TEXT
)
""")
db.commit()

# ---------------- SERVER SETUP ---------------- #
server = socket.socket()
server.bind(("localhost", 12345))
server.listen()

clients = {}  # socket -> username

print("Server started...")


# ---------------- BROADCAST ---------------- #
def broadcast(message, sender=None):
    for client in list(clients):
        if client != sender:
            try:
                client.send(message)
            except:
                client.close()
                del clients[client]


# ---------------- HANDLE CLIENT ---------------- #
def handle_client(client):
    try:
        # ---- GET USERNAME ---- #
        username = client.recv(4096).decode()
        clients[client] = username

        print(f"{username} joined")

        # ---- SEND CHAT HISTORY (FIXED LINE BREAKS) ---- #
        cursor.execute(
            "SELECT username, message, timestamp FROM messages ORDER BY id ASC"
        )
        history = cursor.fetchall()

        for user, msg, time in history:
            formatted = f"[{time}] {user}: {msg}\n"
            client.send(formatted.encode())

        # ---- JOIN MESSAGE ---- #
        join_msg = f"> {username} joined the chat\n"
        broadcast(join_msg.encode(), client)

    except:
        client.close()
        return

    # ---------------- MESSAGE LOOP ---------------- #
    while True:
        try:
            message = client.recv(4096).decode()

            if not message:
                break

            sender = clients[client]

            # -------- PRIVATE MESSAGE -------- #
            if message.startswith("/msg "):
                parts = message.split(" ", 2)
                if len(parts) < 3:
                    continue

                target_name = parts[1]
                private_msg = parts[2]

                target_client = None
                for c, name in clients.items():
                    if name == target_name:
                        target_client = c
                        break

                if target_client:
                    target_client.send(
                        f"[PM] {sender}: {private_msg}\n".encode()
                    )
                    client.send(
                        f"[PM to {target_name}] {private_msg}\n".encode()
                    )

                continue

            # -------- NORMAL MESSAGE -------- #
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            full_message = f"{sender}: {message}\n"

            print(full_message.strip())

            # save to DB
            cursor.execute(
                "INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)",
                (sender, message, timestamp)
            )
            db.commit()

            broadcast(full_message.encode(), client)

        except:
            username = clients.get(client, "Unknown")

            print(f"{username} disconnected")

            del clients[client]
            client.close()

            leave_msg = f"> {username} left the chat\n"
            broadcast(leave_msg.encode(), client)
            break


# ---------------- ACCEPT CONNECTIONS ---------------- #
def receive_connections():
    while True:
        client, addr = server.accept()
        print("Connected:", addr)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


receive_connections()