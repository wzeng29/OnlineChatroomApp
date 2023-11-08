# Assignment: UDP Simple Chat Room - UDP Client Code Implementation

# Libraries and Imports
import socket
import argparse
import select
import threading

def send_message(client_socket, clientname, server_addr, server_port):
    while True:
        message = input("Enter your message: ")
        if message.lower() == "exit":
            break

        message = f"{clientname}: {message}"
        client_socket.sendto(message.encode('utf-8'), (server_addr, server_port))

def receive_messages(client_socket, clientname):
    while True:
        try:
            readable, _, _ = select.select([client_socket], [], [], 1)
            if client_socket in readable:
                message, server_addr = client_socket.recvfrom(1024)
                message = message.decode('utf-8')
                if not message.startswith(clientname):
                    print(f"Received message from {server_addr}: {message}")
        except Exception as e:
            print(e)
            break

# Main Code
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='UDP Chat Client')
    parser.add_argument('name', help='Your username')
    args = parser.parse_args()
    clientname = args.name

    serverAddr = '127.0.0.1'
    serverPort = 9301 

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

    print(f"Welcome, {clientname}! You can start chatting. Type 'exit' to quit.")


    send_thread = threading.Thread(target=send_message, args=(clientSocket, clientname, serverAddr, serverPort))
    receive_thread = threading.Thread(target=receive_messages, args=(clientSocket,clientname))

    send_thread.start()
    receive_thread.start()
    send_thread.join()
    receive_thread.join()
    clientSocket.close()
