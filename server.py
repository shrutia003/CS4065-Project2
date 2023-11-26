import socket
import threading
import time

# Function to handle client connections
def handle_client(client_socket, clients, messages):
    # Placeholder logic for handling a new client
    username = client_socket.recv(1024).decode('utf-8')  # Receive the username from the client
    clients.append((username, client_socket))  # Add the client to the list

    # Notify all clients about the new user
    broadcast(f"[SERVER] {username} has joined the group.", clients, client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'leave':
                clients.remove((username, client_socket))
                broadcast(f"[SERVER] {username} has left the group.", clients, client_socket)
                break
            elif message.startswith('post'):
                # Extract the message content and post it to the group
                post_message(username, message, clients, messages)
            elif message == 'retrieve':
                # Retrieve the last 2 messages and send them to the client
                retrieve_messages(client_socket, clients, messages)
            else:
                broadcast(f"{username}: {message}", clients, client_socket)
        except ConnectionResetError:
            # Handle client disconnection
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
                # Handle any potential errors while sending the message
                pass

# Function to post a message to the group
def post_message(username, message, clients, messages):
    # Extract the message content from the command (assuming the format is "post subject content")
    _, subject, content = message.split(' ', 2)

    # Generate a unique message ID (for simplicity, using the current timestamp)
    message_id = int(time.time() * 1000)

    # Create the message string in the specified format
    formatted_message = f"{message_id}, {username}, {time.strftime('%Y-%m-%d %H:%M:%S')}, {subject}"

    # Add the message to the list
    messages.append(formatted_message)

    # Broadcast the message to all clients in the group
    broadcast(formatted_message, clients, None)

# Function to retrieve the last 2 messages and send them to the client
def retrieve_messages(client_socket, clients, messages):
    # Get the last 2 messages
    recent_messages = messages[-2:]

    # Send the messages to the client
    for msg in recent_messages:
        try:
            client_socket.send(msg.encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] Failed to send message to client: {e}")
            pass

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
        
        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, clients, messages))
        client_handler.start()

# Start the server
start_server()