import socket
import threading
from cryptography.fernet import Fernet

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Receiving the encryption key from the server
key = client.recv(1024)
cipher_suite = Fernet(key)


# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024)
            decrypted_message = cipher_suite.decrypt(message).decode('ascii')
            if decrypted_message == 'NICK':
                client.send(cipher_suite.encrypt(nickname.encode('ascii')))
            else:
                print(decrypted_message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        encrypted_message = cipher_suite.encrypt(message.encode('ascii'))
        client.send(encrypted_message)


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
