import socket
import threading
import time

# Function to handle client connections
def handle_client(client_socket, clients, messages):
    username = client_socket.recv(1024).decode('utf-8')  # Receive the username from the client
    clients.append((username, client_socket))  # Add the client to the list

    # Notify all clients about the new user
    broadcast(f"[SERVER] {username} has joined the group.", clients, client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')

            if message.startswith('%post'):
                post_message(username, message, clients, messages)
            elif message == '%users':
                send_user_list(client_socket, clients)
            elif message.startswith('%message'):
                send_specific_message(client_socket, messages, message.split(' ')[1])
            elif message == '%leave':
                clients.remove((username, client_socket))
                broadcast(f"[SERVER] {username} has left the group.", clients, client_socket)
                break
            else:
                broadcast(f"{username}: {message}", clients, client_socket)

        except ConnectionResetError:
            clients.remove((username, client_socket))
            broadcast(f"[SERVER] {username} has left the group.", clients, client_socket)
            break

# Function to broadcast a message to all clients except the sender
def broadcast(message, clients, sender_socket):
    for _, client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                pass  # Handle any potential errors while sending the message

# Function to post a message to the group
def post_message(username, message, clients, messages):
    parts = message.split(' ', 2)
    if len(parts) == 3 and parts[0] == '%post':
        _, subject, content = parts

        message_id = int(time.time() * 1000)
        formatted_message = f"{message_id}, {username}, {time.strftime('%Y-%m-%d %H:%M:%S')}, {subject}: {content}"
        formatted_messaged = f"{message_id}, {username}, {time.strftime('%Y-%m-%d %H:%M:%S')}, {subject}"
        messages.append(formatted_message)
        broadcast(formatted_messaged, clients, None)
    else:
        print(f"Invalid post format: {message}")

# Function to send a list of users to a client
def send_user_list(client_socket, clients):
    users = [username for username, _ in clients]
    user_list = ", ".join(users)
    client_socket.send(f"[SERVER] Current users: {user_list}".encode('utf-8'))

# Function to send a specific message by ID
def send_specific_message(client_socket, messages, message_id):
    message_id = int(message_id)
    for message in messages:
        # Split the message string into components
        parts = message.split(', ', 3)
        if len(parts) == 4 and int(parts[0]) == message_id:
            # Extracting the content from the last part
            content = parts[3].split(': ', 1)[1] if ': ' in parts[3] else parts[3]
            client_socket.send(content.encode('utf-8'))
            return
    client_socket.send("[SERVER] Message not found.".encode('utf-8'))
# Main server function
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12345))  # Change the IP and port as needed
    server.listen(5)

    print('[SERVER] Server listening on port 12345...')

    clients = []  # List to store connected clients
    messages = []  # List to store posted messages

    while True:
        client_socket, addr = server.accept()
        print(f'[SERVER] Accepted connection from {addr}')

        client_handler = threading.Thread(target=handle_client, args=(client_socket, clients, messages))
        client_handler.start()

# Start the server
if __name__ == "__main__":
    start_server()