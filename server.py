#!/bin/python3
import socket
import threading
from cryptography.fernet import Fernet

# Connection Data
host = '127.0.0.1'
port = 55555

# Generate a key for encryption and decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message, client_socket=None):
    encrypted_message = cipher_suite.encrypt(message)
    for client in clients:
        if client != client_socket:
            client.send(encrypted_message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            decrypted_message = cipher_suite.decrypt(message).decode('ascii')
            broadcast(decrypted_message.encode('ascii'), client)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left!'.encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Send encryption key to the client
        client.send(key)

        # Request And Store Nickname
        client.send(cipher_suite.encrypt('NICK'.encode('ascii')))
        nickname = cipher_suite.decrypt(client.recv(1024)).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined!".encode('ascii'))
        client.send(cipher_suite.encrypt('Connected to server!'.encode('ascii')))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()