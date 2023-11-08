
import select
import sys
import socket
import argparse
import threading

def receive_messages(client_socket,clientname):
    while True:
        try:
            readable, _, _ = select.select([client_socket], [], [], 1)
            if client_socket in readable:
                message, server_addr = client_socket.recvfrom(1024)
                message = message.decode('utf-8')
                if not message.startswith(clientname):
                    print(f"Received message from {message}")
        except Exception as e:
            print(e)
            break

def send_messages(clientSocket, clientName):
    while True:
        message = input()
        if message == 'exit':
            clientSocket.send('exit'.encode())
            break
        clientSocket.send(f'{clientName}: {message}'.encode())
      
def run(clientSocket, clientName):

    receive_thread = threading.Thread(target=receive_messages, args=(clientSocket,client_name))
    receive_thread.start()


    send_thread = threading.Thread(target=send_messages, args=(clientSocket, clientName))
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    clientSocket.close()

# Main Code
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argument Parser')
    parser.add_argument('name') 
    args = parser.parse_args()
    client_name = args.name
    server_addr = '127.0.0.1'
    server_port = 9301

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_addr, server_port))

    run(client_socket, client_name)
