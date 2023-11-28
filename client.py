import socket
import threading
import sys

# Main client function
def start_client():
    running = [True]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Flag to track the connection status
    connected = False

    # Get the desired username from the user
    username = input("Enter your username: ")

    # Send the username once connected
    def send_username():
        client.send(username.encode('utf-8'))

    # Function to handle user input and send messages to the server
    def user_input():
        nonlocal connected
        while True:
            message = input()
            if message.startswith('%connect') and not connected:
                _, address, port = message.split(' ')
                try:
                    client.connect((address, int(port)))
                    print(f"[CLIENT] Connected to {address}:{port}")
                    send_username()
                    connected = True
                    start_receiving()  # Start receiving messages after connection
                except Exception as e:
                    print(f"[ERROR] Failed to connect: {e}")
            elif message.lower() == '%exit':
                client.close()
                break
            elif connected:
                client.send(message.encode('utf-8'))  # Send all messages to the server
            else:
                print("[CLIENT] Not connected to a server.")

    # Function to receive and display messages from the server
    def receive_messages():
        while running[0]:
            try:
                message = client.recv(1024).decode('utf-8')
                print(message)
            except ConnectionResetError:
                print("[CLIENT] Connection to the server lost.")
                break
            except ConnectionAbortedError:
                print("[CLIENT] Connection to the server lost.")
                break

    # Function to start receiving messages
    def start_receiving():
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()

    # Create thread for handling user input
    input_thread = threading.Thread(target=user_input)
    input_thread.start()
    input_thread.join()

    if connected:
        client.close()

# Start the client
if __name__ == "__main__":
    start_client()
