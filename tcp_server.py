# Libraries and Imports
import socket
import threading

# Global Variables
# If needed, you can define global variables here.

# Function to handle individual clients
def client_handler(client_socket, clients, username):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            formatted_message = f" {message}"  # Include username in the message
            print(formatted_message)  # Output the message to the server's console
            for client in clients:
                if client != client_socket:
                    client.send(formatted_message.encode())
        except Exception as e:
            print(e)
            break
    client_socket.close()
    clients.remove(client_socket)

# Main Server Function
def run(server_socket, server_port):
    clients = []

    while True:
        client_socket, client_addr = server_socket.accept()
        # Receive the initial message to get the username
        initial_message = client_socket.recv(1024).decode('utf-8')
        parts = initial_message.split(':')
        if len(parts) == 2:
            username, message_content = parts
        else:
            username = "Unknown"  # If the message format is invalid
        clients.append(client_socket)
        print(f"User {username} connected from {client_addr}")
        client_handler_thread = threading.Thread(target=client_handler, args=(client_socket, clients, username))
        client_handler_thread.start()

# Main Code
if __name__ == "__main__":
    
    server_port = 9301
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP socket.

    # Attempt to bind the server socket to the specified address and port
    while True:
        try:
            server_socket.bind(('127.0.0.1', server_port))
            server_socket.listen(3) 
            break  
        except Exception as e:
            print(f"Port {server_port} is already in use. Trying the next port.")
            server_port += 1
    print("This is the server side.")
    print(f"I'm ready to receive on port {server_port}.")
    run(server_socket, server_port) 