import socket
import threading
import sys

# Function to handle user input and send messages to the server
def user_input(client_socket):
    try:
        while True:
            message = input()
            client_socket.send(message.encode('utf-8'))
            if message.lower() == '%exit':
                break
    except KeyboardInterrupt:
        pass

# Function to receive and display messages from the server
def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
    except ConnectionResetError:
        print("[CLIENT] Connection to the server lost.")
        sys.exit()

# Main client function
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12345))  # Connect to the server IP and port

    print('[CLIENT] Connected to the server.')

    # Create separate threads for handling user input and receiving messages
    input_thread = threading.Thread(target=user_input, args=(client,))
    receive_thread = threading.Thread(target=receive_messages, args=(client,))

    input_thread.start()
    receive_thread.start()

    input_thread.join()
    receive_thread.join()

    client.close()

# Start the client
start_client()