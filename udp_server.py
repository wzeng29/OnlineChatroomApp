# Assignment: UDP Simple Chat Room - UDP Server Code Implementation

# Libraries and Imports
import socket
import select

def run(server_socket, server_port):
    server_socket.bind(('0.0.0.0', server_port)) 
    print(f"UDP Server is running on port {server_port}")

    clients = set()  
    while True:
        try:
            readable, _, _ = select.select([server_socket], [], [], 1)
            if server_socket in readable:
                message, client_addr = server_socket.recvfrom(1024)
                message = message.decode('utf-8')
                
                parts = message.split(':', 1)
                if len(parts) == 2:
                    username, message_content = parts
                    print(f"User {username} connected from {client_addr}")
                else:
                    username = "Unknown" 

                print(f"Received message from {username}: {message_content}")

                for client in clients:
                    if client != server_socket:
                        server_socket.sendto(message.encode('utf-8'), client)

                clients.add(client_addr) 
        except Exception as e:
            print(e)

# Main Code
if __name__ == "__main__":
    serverPort = 9301  
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    run(serverSocket, serverPort)
